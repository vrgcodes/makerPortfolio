package com.example.astroguard

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.astroguard.databinding.ActivityDashboardViewBinding
import java.io.IOException
import java.util.UUID


class dashboardView : AppCompatActivity() {
    private val binding: ActivityDashboardViewBinding by lazy {
        ActivityDashboardViewBinding.inflate(layoutInflater)
    }
    private var bluetoothSocket: BluetoothSocket? = null
    private val KNOWN_SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        binding.imageButton.setOnClickListener{
            startActivity(Intent(this,faceRecogCamera::class.java))
        }

        binding.lock.setOnClickListener{
            sendData("Lock door")

        }

        binding.unlock.setOnClickListener{
            startActivity(Intent(this,faceRecogUnlock::class.java))
        }
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