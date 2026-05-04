package com.example.uvindexapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.example.uvindexapp.ui.theme.UVIndexAppTheme
import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            UVIndexAppTheme {
                UVScreen()
            }
        }
    }
}

@Composable
fun UVScreen() {
    Box(
        modifier = androidx.compose.ui.Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "UV 앱 시작됨!",
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold
        )
    }
}
@Composable
fun UVScreen() {
    val context = LocalContext.current
    var locationGranted by remember { mutableStateOf(false) }

    // 권한 요청 런처
    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        locationGranted = isGranted
    }

    // 앱 실행 시 권한 체크 및 요청
    LaunchedEffect(Unit) {
        val permissionCheck = ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.ACCESS_FINE_LOCATION
        )
        if (permissionCheck == PackageManager.PERMISSION_GRANTED) {
            locationGranted = true
        } else {
            launcher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
        }
    }

    // 화면 UI
    Box(
        modifier = androidx.compose.ui.Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        if (locationGranted) {
            Text(
                text = "위치 권한 승인됨!\nUV 데이터 가져올 준비 완료",
                fontSize = 25.sp,
                fontWeight = FontWeight.Bold
            )
        } else {
            Text(
                text = "위치 권한 필요",
                fontSize = 25.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

