import React, { useState } from 'react';
import QrReader from 'react-qr-reader';

const QRCodeScanner = () => {
  const [showScanner, setShowScanner] = useState(false);
  const [scanResult, setScanResult] = useState('');

  const handleScan = (data) => {
    if (data) {
      setScanResult(data);
      setShowScanner(false); // Hide scanner after successful scan
    }
  };

  const handleError = (err) => {
    console.error(err);
  };

  return (
    <div>
      <button onClick={() => setShowScanner(true)}>Scan QR Code</button>
      {showScanner && (
        <div>
          <QrReader
            delay={300}
            onError={handleError}
            onScan={handleScan}
            style={{ width: '100%' }}
          />
          <button onClick={() => setShowScanner(false)}>Close Scanner</button>
        </div>
      )}
      {scanResult && <p>Scanned Result: {scanResult}</p>}
    </div>
  );
};

export default QRCodeScanner;