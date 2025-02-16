import React, { useState } from "react";
import axios from "axios";
import { RadialBarChart, RadialBar, Legend } from "recharts";

export default function Speedometer() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const iniciarTeste = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/testar_internet");
      setData(response.data);
    } catch (error) {
      console.error("Erro ao testar a internet", error);
    }
    setLoading(false);
  };

  const chartData = data
    ? [
        { name: "Download", value: data.download, fill: "#8884d8" },
        { name: "Upload", value: data.upload, fill: "#82ca9d" },
        { name: "Ping", value: data.ping, fill: "#ff7300" },
        { name: "Jitter", value: data.jitter, fill: "#d0ed57" },
      ]
    : [];

  return (
    <div className="flex flex-col items-center justify-center p-5">
      <h1 className="text-2xl font-bold mb-4">Teste de Velocidade da Internet</h1>
      <button
        onClick={iniciarTeste}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
      >
        {loading ? "Testando..." : "Iniciar Teste"}
      </button>

      {data && (
        <div className="mt-6">
          <RadialBarChart width={300} height={300} innerRadius="10%" outerRadius="100%" data={chartData}>
            <RadialBar minAngle={15} background clockWise dataKey="value" />
            <Legend iconSize={10} layout="horizontal" align="center" />
          </RadialBarChart>

          <p className="text-lg mt-4">📡 Download: {data.download} Mbps</p>
          <p className="text-lg">🚀 Upload: {data.upload} Mbps</p>
          <p className="text-lg">⚡ Ping: {data.ping} ms</p>
          <p className="text-lg">📉 Jitter: {data.jitter} ms</p>
          <p className="text-lg">❌ Perda de Pacotes: {data.perda_pacotes} %</p>
        </div>
      )}
    </div>
  );
}
