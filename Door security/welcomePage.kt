package com.example.astroguard

import android.content.Intent
import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.astroguard.databinding.ActivityWelcomePageBinding


class welcomePage : AppCompatActivity() {
    private val binding:ActivityWelcomePageBinding by lazy{
        ActivityWelcomePageBinding.inflate(layoutInflater)
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(binding.root)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        binding.loginEntry.setOnClickListener{
            startActivity(Intent(this,login::class.java))
            finish()
        }

        binding.registerEntry.setOnClickListener{
            startActivity(Intent(this,register::class.java))
            finish()
        }
    }


}
