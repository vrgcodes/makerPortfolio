package com.example.astroguard

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.astroguard.databinding.ActivityFaceRecogCameraBinding
import com.example.astroguard.databinding.ActivityFaceRecogUnlockBinding
import com.google.firebase.auth.FirebaseAuth
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import okhttp3.Response
import org.json.JSONException
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.util.UUID
import java.util.concurrent.TimeUnit

class faceRecogUnlock : AppCompatActivity() {
    private val binding: ActivityFaceRecogUnlockBinding by lazy {
        ActivityFaceRecogUnlockBinding.inflate(layoutInflater)
    }

    private var imageCapture: ImageCapture? = null
    private lateinit var auth: FirebaseAuth


    private var bluetoothSocket: BluetoothSocket? = null
    private val KNOWN_SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    @RequiresApi(Build.VERSION_CODES.S)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        val requestPermissionLauncher = registerForActivityResult(
            ActivityResultContracts.RequestPermission()
        ) { isGranted: Boolean ->
            if (isGranted) {
                startCamera()
            } else {
                Toast.makeText(this, "Camera permission denied", Toast.LENGTH_SHORT).show()
                finish()
            }
        }

        when {
            ContextCompat.checkSelfPermission(
                this, Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED -> startCamera()
            else -> requestPermissionLauncher.launch(Manifest.permission.CAMERA)
        }



        binding.captureButton.setOnClickListener{
            takePhoto()
        }

    }
    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener({
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()
            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(binding.cameraPreview.surfaceProvider)
            }

            imageCapture = ImageCapture.Builder().build()

            val cameraSelector = CameraSelector.DEFAULT_FRONT_CAMERA

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageCapture
                )
            } catch (e: Exception) {
                Log.e("CameraActivity", "Failed to start camera: ", e)
            }
        }, ContextCompat.getMainExecutor(this))
    }
    @RequiresApi(Build.VERSION_CODES.S)
    private fun takePhoto() {
        auth = FirebaseAuth.getInstance()
        val userEmail = auth.currentUser?.email

        val imageCapture = imageCapture ?: return

        val photoFile = File.createTempFile("photo", ".jpg",cacheDir)

        val outputOptions = ImageCapture.OutputFileOptions.Builder(photoFile).build()

        imageCapture.takePicture(
            outputOptions,
            ContextCompat.getMainExecutor(this),
            object : ImageCapture.OnImageSavedCallback {
                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    val byteArray = photoFile.readBytes()
                    if (userEmail != null) {
                        sendImagetoServer(byteArray,userEmail)
                    }
                }



                override fun onError(exception: ImageCaptureException) {
                    Log.e("CameraActivity", "Photo capture failed: ${exception.message}", exception)
                }
            }
        )


    }
    private fun sendImagetoServer(imageByteArray:ByteArray, emailID:String){
        val client = OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(60, TimeUnit.SECONDS)
            .build()

        val mediaType = "image/jpeg".toMediaTypeOrNull()

        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("email", emailID)
            .addFormDataPart("image", "photo.jpg", RequestBody.create(mediaType,imageByteArray))
            .build()

        val request = Request.Builder()
            .url("http://192.168.1.14:5000/recognize")
            .post(requestBody)
            .build()

        Log.d("HTTP_Request", "Request URL: ${request.url}")
        Log.d("HTTP_Request", "Request Body: ${requestBody.toString()}")

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("Server", "Failed to upload image: ${e.message}")
                runOnUiThread {
                    Toast.makeText(applicationContext, "Failed to upload image: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (response.isSuccessful) {
                        val responseBody = response.body?.string()
                        try {
                            val jsonResponse = JSONObject(responseBody)
                            val message = jsonResponse.getString("message")
                            Log.d("Server", message)
                            if (message == "Face recognized successfully"){
                                runOnUiThread {
                                    Toast.makeText(applicationContext, "Unlocking the door.", Toast.LENGTH_LONG).show()
                                    sendData("Unlock door")
                                    val intent = Intent(this@faceRecogUnlock, dashboardView::class.java)
                                    startActivity(intent)
                                }
                            }
                            else{
                                runOnUiThread {
                                    Toast.makeText(applicationContext, message, Toast.LENGTH_LONG).show()
                                }
                            }

                        } catch (e: JSONException) {
                            Log.e("Server", "Failed to parse JSON: ${e.message}")
                            runOnUiThread {
                                Toast.makeText(applicationContext, "Server returned invalid response", Toast.LENGTH_LONG).show()
                            }
                        }
                    } else {
                        Log.e("Server", "Error uploading image: ${response.message}")
                        runOnUiThread {
                            Toast.makeText(applicationContext, "Error uploading image: ${response.message}", Toast.LENGTH_LONG).show()
                        }
                    }
                }
            }

        })


    }
    private fun sendData(messageToSend:String){
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
            if (ActivityCompat.checkSelfPermission(
                    this,
                    android.Manifest.permission.BLUETOOTH_CONNECT
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(android.Manifest.permission.BLUETOOTH_CONNECT),
                    1
                )
                return
            }
        }

        val bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()
        if (bluetoothAdapter == null) {
            Toast.makeText(this, "Bluetooth not supported", Toast.LENGTH_SHORT).show()
            return
        }

        val pairedDevices = bluetoothAdapter.bondedDevices
        var hc05_address: String? = null

        if(pairedDevices.isNotEmpty()){
            for(device in pairedDevices){
                val name = device.name
                val address = device.address
                if(name.equals("HC-05", ignoreCase = true)){
                    hc05_address = address
                    break

                }
            }
        }

        if(hc05_address==null){
            Toast.makeText(this,"Bluetooth module is not paired. Pair the device first.", Toast.LENGTH_SHORT).show()
            return
        }

        val hc05: BluetoothDevice? = bluetoothAdapter.bondedDevices.find{it.address==hc05_address}

        try {
            if (hc05 != null) {

                bluetoothSocket = hc05.createRfcommSocketToServiceRecord(KNOWN_SPP_UUID)
            }
            bluetoothSocket?.connect()
            Toast.makeText(this, "Connected to HC-05", Toast.LENGTH_SHORT).show()
        } catch (e: IOException) {
            Toast.makeText(this, "Failed to connect: ${e.message}", Toast.LENGTH_SHORT).show()
            return
        }
        try {
            bluetoothSocket?.outputStream?.write(messageToSend.toByteArray())
            Toast.makeText(this, "Message sent: $messageToSend", Toast.LENGTH_SHORT).show()
        } catch (e: IOException) {
            Toast.makeText(this, "Failed to send message: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }
    override fun onDestroy() {
        super.onDestroy()
        try {
            bluetoothSocket?.close()
        } catch (e: IOException) {
            // Ignore
        }
    }
}
