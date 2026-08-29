"use client";

import { Battery, BatteryWarning, Signal, Wifi, WifiOff } from "lucide-react";
import { Nodo } from "@/types";

// Datos simulados para visualizar la tabla antes de conectar la base de datos
const mockNodos: Nodo[] = [
  {
    id: "AGV-001",
    fundo: "Parcela Experimental U. de Chile",
    sector: "Sector 1 - Paltos",
    estado: "online",
    voltajeBateria: 3.2,
    nivelBateria: 95,
    rssi: -65,
    ultimaConexion: new Date().toISOString(),
  },
  {
    id: "AGV-002",
    fundo: "Parcela Experimental U. de Chile",
    sector: "Sector 2 - Cerezos",
    estado: "offline",
    voltajeBateria: 2.8,
    nivelBateria: 15,
    rssi: -120,
    ultimaConexion: new Date(Date.now() - 3600000 * 4).toISOString(), // 4 horas atrás
  }
];

export default function DiagnosticoRed() {
  return (
    <main className="p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Diagnóstico de Red LoRa</h1>
        <p className="text-slate-400">Monitoreo del estado físico y telemetría de los nodos en terreno.</p>
      </header>

      <div className="bg-slate-900 rounded-lg border border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-800 text-slate-400 font-medium border-b border-slate-700">
              <tr>
                <th className="px-6 py-4">ID Nodo</th>
                <th className="px-6 py-4">Ubicación</th>
                <th className="px-6 py-4">Estado</th>
                <th className="px-6 py-4">Batería (LiFePO4)</th>
                <th className="px-6 py-4">Señal (RSSI)</th>
                <th className="px-6 py-4">Última Conexión</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {mockNodos.map((nodo) => (
                <tr key={nodo.id} className="hover:bg-slate-800/50 transition-colors">
                  <td className="px-6 py-4 font-mono font-medium text-white">{nodo.id}</td>
                  <td className="px-6 py-4">
                    <div className="flex flex-col">
                      <span className="font-medium text-slate-200">{nodo.sector}</span>
                      <span className="text-xs text-slate-500">{nodo.fundo}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                      nodo.estado === 'online' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'
                    }`}>
                      {nodo.estado === 'online' ? <Wifi className="w-3.5 h-3.5" /> : <WifiOff className="w-3.5 h-3.5" />}
                      {nodo.estado.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      {nodo.nivelBateria > 20 ? (
                        <Battery className="w-4 h-4 text-green-400" />
                      ) : (
                        <BatteryWarning className="w-4 h-4 text-red-400" />
                      )}
                      <span>{nodo.nivelBateria}%</span>
                      <span className="text-xs text-slate-500">({nodo.voltajeBateria}V)</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <Signal className={`w-4 h-4 ${nodo.rssi > -90 ? 'text-green-400' : 'text-yellow-400'}`} />
                      <span>{nodo.rssi} dBm</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-slate-400">
                    {new Date(nodo.ultimaConexion).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}