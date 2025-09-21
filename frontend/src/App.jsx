const sampleProducts = [
  { sku: 'SKU-1001', name: 'Laptop Pro 15', stock: 10, minStock: 2, price: 1499.99 },
  { sku: 'SKU-1002', name: 'Monitor UltraWide 34in', stock: 15, minStock: 3, price: 749.5 },
  { sku: 'SKU-1003', name: 'Teclado Mecanico RGB', stock: 40, minStock: 10, price: 129.99 },
  { sku: 'SKU-1004', name: 'Mouse Inalambrico MX', stock: 8, minStock: 5, price: 99.99 },
];

const formatCurrency = (value) =>
  new Intl.NumberFormat('es-MX', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
  }).format(value);

function App() {
  const totalInventoryValue = sampleProducts.reduce(
    (sum, product) => sum + product.price * product.stock,
    0,
  );
  const lowStockItems = sampleProducts.filter((product) => product.stock <= product.minStock);

  return (
    <div className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800 bg-slate-900/70 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.25em] text-sky-300">ERP Stack</p>
            <h1 className="mt-1 text-2xl font-semibold text-white">Panel de Inventario</h1>
          </div>
          <button
            type="button"
            className="rounded-full bg-sky-500 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-sky-500/30 transition hover:bg-sky-400"
          >
            + Nuevo producto
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-10">
        <section className="grid gap-6 md:grid-cols-3">
          <article className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-black/20">
            <p className="text-sm font-medium text-slate-400">SKUs totales</p>
            <p className="mt-3 text-4xl font-bold text-slate-50">{sampleProducts.length}</p>
            <p className="mt-2 text-sm text-slate-500">Productos activos en catalogo</p>
          </article>

          <article className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-black/20">
            <p className="text-sm font-medium text-slate-400">Valor estimado</p>
            <p className="mt-3 text-4xl font-bold text-slate-50">{formatCurrency(totalInventoryValue)}</p>
            <p className="mt-2 text-sm text-slate-500">Considerando stock actual</p>
          </article>

          <article className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-black/20">
            <p className="text-sm font-medium text-slate-400">Alertas de stock</p>
            <p className="mt-3 text-4xl font-bold text-slate-50">{lowStockItems.length}</p>
            <p className="mt-2 text-sm text-slate-500">Productos por debajo del minimo</p>
          </article>
        </section>

        <section className="mt-10">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-white">Inventario reciente</h2>
              <p className="text-sm text-slate-500">Muestra de datos de ejemplo para pruebas del CRUD</p>
            </div>
            <button
              type="button"
              className="rounded-full border border-slate-700 px-4 py-1.5 text-sm font-medium text-slate-200 transition hover:border-slate-500"
            >
              Exportar CSV
            </button>
          </div>

          <div className="mt-4 overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 shadow-xl shadow-black/20">
            <table className="min-w-full divide-y divide-slate-800">
              <thead className="bg-slate-900/70">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-400">SKU</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-400">Producto</th>
                  <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">Stock</th>
                  <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">Stock minimo</th>
                  <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wider text-slate-400">Precio</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {sampleProducts.map((product) => {
                  const isLowStock = product.stock <= product.minStock;
                  return (
                    <tr key={product.sku} className="hover:bg-slate-900/80">
                      <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-slate-200">
                        {product.sku}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-300">{product.name}</td>
                      <td className="px-6 py-4 text-right text-sm font-semibold text-slate-100">
                        {product.stock}
                      </td>
                      <td className="px-6 py-4 text-right text-sm">
                        <span className={isLowStock ? 'rounded-full bg-rose-900/60 px-3 py-1 text-rose-200' : 'rounded-full bg-emerald-900/60 px-3 py-1 text-emerald-200'}>
                          {product.minStock}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right text-sm font-semibold text-slate-100">
                        {formatCurrency(product.price)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;