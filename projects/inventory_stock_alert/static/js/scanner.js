// Barcode scanner using jsQR
const JSQR_CDN = 'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js';

function loadJsQR(cb) {
    if (window.jsQR) return cb();
    const s = document.createElement('script');
    s.src = JSQR_CDN;
    s.onload = cb;
    document.head.appendChild(s);
}

let scanStream = null;
let scanInterval = null;

function openScanner() {
    document.getElementById('scanner-modal').classList.remove('hidden');
    loadJsQR(startCamera);
}

function closeScanner() {
    document.getElementById('scanner-modal').classList.add('hidden');
    if (scanStream) { scanStream.getTracks().forEach(t => t.stop()); scanStream = null; }
    if (scanInterval) { clearInterval(scanInterval); scanInterval = null; }
}

async function startCamera() {
    const video = document.getElementById('scanner-video');
    const canvas = document.getElementById('scanner-canvas');
    try {
        scanStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
        video.srcObject = scanStream;
        video.play();
        scanInterval = setInterval(() => {
            if (video.readyState !== video.HAVE_ENOUGH_DATA) return;
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            const img = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(img.data, img.width, img.height);
            if (code) {
                clearInterval(scanInterval);
                handleBarcode(code.data);
            }
        }, 300);
    } catch (e) {
        document.getElementById('scan-result').textContent = 'Camera access denied.';
    }
}

async function handleBarcode(barcode) {
    document.getElementById('scan-result').textContent = `Scanned: ${barcode}`;
    // If on form page, fill barcode input
    const barcodeInput = document.getElementById('barcode-input');
    if (barcodeInput) {
        barcodeInput.value = barcode;
        closeScanner();
        return;
    }
    // Otherwise look up item
    const res = await fetch(`/api/barcode/${barcode}`);
    const data = await res.json();
    if (data.found) {
        document.getElementById('scan-result').textContent =
            `✅ Found: ${data.name} — ${data.quantity} ${data.unit}`;
    } else {
        document.getElementById('scan-result').textContent =
            `❌ Not found. Barcode: ${barcode}`;
    }
    setTimeout(closeScanner, 2500);
}
