import { useState, useEffect } from "react";
import { api } from "./api";
import { useForm } from "react-hook-form";

export default function App() {
  // Estados para búsqueda y paginación
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Estados para clientes y formulario
  const [clientes, setClientes] = useState([]);
  const [selected, setSelected] = useState(null);
  const { register, handleSubmit, reset } = useForm();

  // Cargar clientes con filtros
  async function loadClientes() {
    const res = await api.get("/clientes", {
      params: { search, page, per_page: 5 }
    });
    setClientes(res.data.clientes);
    setTotalPages(res.data.pages);
  }

  useEffect(() => {
    loadClientes();
  }, [page, search]); // se recarga cuando cambian

  // Guardar cliente
  async function onSubmit(data) {
    if (selected) {
      await api.put(`/clientes/${selected.id}`, data);
    } else {
      await api.post("/clientes", data);
    }
    reset();
    setSelected(null);
    loadClientes();
  }

  // Eliminar cliente
  async function eliminar(id) {
    await api.delete(`/clientes/${id}`);
    loadClientes();
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">ABM de Clientes</h1>

      {/* Buscador */}
      <div className="mb-4 flex gap-2">
        <input
          className="border p-2 flex-1"
          placeholder="Buscar por razón social o CUIT"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded"
          onClick={() => { setPage(1); loadClientes(); }}
        >
          Buscar
        </button>
        <button
          className="bg-gray-400 text-white px-4 py-2 rounded"
          onClick={() => { setSearch(""); setPage(1); loadClientes(); }}
        >
          Limpiar
        </button>
      </div>

      {/* Paginación */}
      <div className="mt-4 flex gap-2 items-center">
        <button
          disabled={page <= 1}
          onClick={() => setPage(page - 1)}
          className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50"
        >
          ← Anterior
        </button>
        <span>Página {page} de {totalPages}</span>
        <button
          disabled={page >= totalPages}
          onClick={() => setPage(page + 1)}
          className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50"
        >
          Siguiente →
        </button>
      </div>

      {/* Formulario */}
      <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-2 gap-4 mb-6 mt-6">
        <input className="border p-2" placeholder="Razón social" {...register("razon_social")} />
        <input className="border p-2" placeholder="CUIT" {...register("cuit")} />
        <input className="border p-2" placeholder="Email" {...register("email")} />
        <input className="border p-2" placeholder="Teléfono" {...register("telefono")} />
        <input className="border p-2 col-span-2" placeholder="Dirección" {...register("direccion")} />
        <label className="flex items-center space-x-2">
          <input type="checkbox" {...register("activo")} />
          <span>Activo</span>
        </label>
        <div className="col-span-2 flex gap-2">
          <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded">Guardar</button>
          <button type="button" onClick={() => { reset(); setSelected(null); }} className="bg-gray-400 text-white px-4 py-2 rounded">
            Cancelar
          </button>
        </div>
      </form>

      {/* Tabla */}
      <table className="w-full border border-gray-300">
        <thead className="bg-gray-100">
          <tr>
            <th className="border px-2 py-1">Razón social</th>
            <th className="border px-2 py-1">CUIT</th>
            <th className="border px-2 py-1">Email</th>
            <th className="border px-2 py-1">Teléfono</th>
            <th className="border px-2 py-1">Activo</th>
            <th className="border px-2 py-1">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {clientes.map(c => (
            <tr key={c.id}>
              <td className="border px-2 py-1">{c.razon_social}</td>
              <td className="border px-2 py-1">{c.cuit}</td>
              <td className="border px-2 py-1">{c.email}</td>
              <td className="border px-2 py-1">{c.telefono}</td>
              <td className="border px-2 py-1">{c.activo ? "Sí" : "No"}</td>
              <td className="border px-2 py-1">
                <button onClick={() => { setSelected(c); reset(c); }} className="text-blue-600 mr-2">Editar</button>
                <button onClick={() => eliminar(c.id)} className="text-red-600">Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
