package com.example.expensetrackersms
import android.util.Log
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Callback
import okhttp3.Call
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException
object NetworkClient {
    // 10.0.2.2 is the special IP the Android EMULATOR uses to reach
    // "localhost" on your actual computer (where FastAPI is running).
    // If testing on a REAL phone instead, replace this with your
    // computer's local network IP, e.g. "http://192.168.1.5:8000"
    private const val BASE_URL = "http://10.0.2.2:8000"

    private val client = OkHttpClient()

    fun sendSmsToBackend(sender: String, smsText: String) {
        val json = JSONObject()
        json.put("sms_text", smsText)
        json.put("sender", sender)

        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)

        val request = Request.Builder()
            .url("$BASE_URL/sms/ingest")
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e("NetworkClient", "Failed to send SMS to backend: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                Log.d("NetworkClient", "Backend response: ${response.code} - ${response.body?.string()}")
                response.close()
            }
        })
    }
}