package com.example.expensetrackersms
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.util.Log
class SmsReceiver : BroadcastReceiver(){
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != Telephony.Sms.Intents.SMS_RECEIVED_ACTION) return

        val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)

        for (sms in messages) {
            val sender = sms.originatingAddress ?: "Unknown"
            val body = sms.messageBody ?: ""

            Log.d("SmsReceiver", "From: $sender | Body: $body")

            // Send it to the backend via NetworkClient (built in the next step)
            NetworkClient.sendSmsToBackend(sender, body)
        }
    }
}