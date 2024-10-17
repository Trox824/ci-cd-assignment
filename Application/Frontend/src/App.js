import React, { useState } from "react";
import axios from "axios";

function App() {
  const [amount, setAmount] = useState("");
  const [fromCurrency, setFromCurrency] = useState("USD");
  const [toCurrency, setToCurrency] = useState("EUR");
  const [convertedAmount, setConvertedAmount] = useState(null);
  const [error, setError] = useState("");

  const handleConvert = async () => {
    setError("");
    setConvertedAmount(null);
    try {
      const response = await axios.get(`http://${window.location.hostname}:8000/convert`, {
        params: {
          amount: parseFloat(amount),
          from_currency: fromCurrency,
          to_currency: toCurrency,
        },
      });
      console.log("API Response:", response.data); // Debugging statement
      if (response.data && response.data.converted_amount !== undefined) {
        setConvertedAmount(response.data.converted_amount);
      } else {
        setError("Invalid response from server");
      }
    } catch (err) {
      console.error("Error:", err); // Debugging statement
      setError(err.response?.data?.detail || "Error during conversion");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">Currency Converter</h1>

        <div className="mb-4">
          <label className="block mb-2 text-sm">Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg"
            placeholder="Enter amount"
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2 text-sm">From Currency</label>
          <input
            type="text"
            value={fromCurrency}
            onChange={(e) => setFromCurrency(e.target.value.toUpperCase())}
            className="w-full px-3 py-2 border rounded-lg"
            placeholder="e.g. USD"
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2 text-sm">To Currency</label>
          <input
            type="text"
            value={toCurrency}
            onChange={(e) => setToCurrency(e.target.value.toUpperCase())}
            className="w-full px-3 py-2 border rounded-lg"
            placeholder="e.g. EUR"
          />
        </div>

        <button
          onClick={handleConvert}
          className="w-full bg-red-500 text-white py-2 rounded-lg mt-4 hover:bg-blue-600"
        >
          Convert
        </button>

        {error && <p className="text-red-500 mt-4">{error}</p>}
        {convertedAmount !== null && (
          <p className="mt-4">
            {amount} {fromCurrency} = {convertedAmount.toFixed(4)} {toCurrency}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
