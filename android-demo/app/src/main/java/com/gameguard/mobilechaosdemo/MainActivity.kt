package com.gameguard.mobilechaosdemo

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Button
import org.json.JSONObject

class MainActivity : Activity() {
    private var level = 12
    private var coins = 500
    private val prefs by lazy { getSharedPreferences("game_state", MODE_PRIVATE) }
    private lateinit var info: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        level = prefs.getInt("level", 12)
        coins = prefs.getInt("coins", 500)
        val layout = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL; setPadding(40, 80, 40, 40) }
        info = TextView(this)
        layout.addView(info)
        val earn = Button(this).apply {
            text = "Earn 10 coins"
            setOnClickListener { coins += 10; persist(); render() }
        }
        layout.addView(earn)
        setContentView(layout)
        render()
    }
    private fun persist() {
        prefs.edit().putInt("level",level).putInt("coins",coins).apply()
    }
    private fun render() {
        info.text = "Mobile Chaos Demo\nLevel: $level\nCoins: $coins"
    }
    private fun logState() {
        val state = JSONObject().put("level",level).put("coins",coins)
        Log.i("MobileChaosDemo", "GAME_STATE:$state")
    }
    override fun onStart() { super.onStart(); logState() }
    override fun onStop() { persist(); super.onStop() }
}
