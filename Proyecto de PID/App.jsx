function App() {
    const [form, setForm] = React.useState(() => {
      const saved = localStorage.getItem('estrategia');
      return saved ? JSON.parse(saved) : {
        numero: '',
        denominacion: '',
        inicio: '',
        fin: '',
        responsable: '',
      };
    });
  
    const [fontSize, setFontSize] = React.useState(14);
    const [bgColor, setBgColor] = React.useState('#ffffff');
    const [textDirection, setTextDirection] = React.useState('ltr');
    const [fontWeight, setFontWeight] = React.useState('normal');
    const [fontStyle, setFontStyle] = React.useState('normal');
    const [textDecoration, setTextDecoration] = React.useState('none');
    const [isVisible, setIsVisible] = React.useState(true);
  
    React.useEffect(() => {
      localStorage.setItem('estrategia', JSON.stringify(form));
    }, [form]);
  
    function handleChange(e) {
      const { name, value } = e.target;
      setForm(prev => ({ ...prev, [name]: value }));
    }
  
    if (!isVisible) {
      return <div className="text-center mt-10">Formulario cerrado.</div>;
    }
  
    return (
      <div className="w-full max-w-screen-lg mx-auto bg-white p-6 sm:p-10 rounded-xl shadow-md relative text-base">
        <div className="absolute top-4 right-4 flex gap-2">
          <button onClick={() => alert('Ampliar')} className="px-2 py-1 border rounded bg-yellow-200 hover:bg-yellow-300">🔍</button>
          <button onClick={() => setIsVisible(false)} className="px-2 py-1 border rounded bg-red-300 hover:bg-red-400">❌</button>
        </div>
  
        <h1 className="text-3xl font-bold mb-6 text-blue-600">Adicionar estrategia</h1>
  
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block font-semibold">No°</label>
            <input type="number" name="numero" value={form.numero} onChange={handleChange} className="w-full border p-3 rounded" required />
          </div>
          <div>
            <label className="block font-semibold">Denominación</label>
            <input type="text" name="denominacion" value={form.denominacion} onChange={handleChange} className="w-full border p-3 rounded" required />
          </div>
        </div>
  
        <div className="mb-6">
          <h2 className="text-xl font-semibold border-b pb-2 mb-4 text-green-500">Datos Generales</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold">Fecha inicio</label>
              <input type="date" name="inicio" value={form.inicio} onChange={handleChange} className="w-full border p-3 rounded" required />
            </div>
            <div>
              <label className="block font-semibold">Fecha fin</label>
              <input type="date" name="fin" value={form.fin} onChange={handleChange} className="w-full border p-3 rounded" required />
            </div>
          </div>
        </div>
  
        <div className="mb-6">
          <h2 className="text-xl font-semibold border-b pb-2 mb-4 text-purple-500">Responsable</h2>
  
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <select className="border p-2 rounded">
              <option>Helvetica</option>
              <option>Arial</option>
              <option>Times New Roman</option>
            </select>
            <select className="border p-2 rounded" onChange={(e) => setFontSize(Number(e.target.value))}>
              <option value="12">12px</option>
              <option value="14">14px</option>
              <option value="16">16px</option>
              <option value="18">18px</option>
            </select>
            <button className="px-3 py-2 border rounded font-bold" onClick={() => setFontWeight(fontWeight === 'bold' ? 'normal' : 'bold')}>B</button>
            <button className="px-3 py-2 border rounded italic" onClick={() => setFontStyle(fontStyle === 'italic' ? 'normal' : 'italic')}>I</button>
            <button className="px-3 py-2 border rounded underline" onClick={() => setTextDecoration(textDecoration === 'underline' ? 'none' : 'underline')}>U</button>
            <button className="px-3 py-2 border rounded" onClick={() => setTextDirection(textDirection === 'ltr' ? 'rtl' : 'ltr')}>↔ Dirección</button>
            <button className="px-3 py-2 border rounded" onClick={() => setFontSize(prev => prev + 2)}>T➕</button>
            <button className="px-3 py-2 border rounded" onClick={() => setFontSize(prev => Math.max(10, prev - 2))}>T➖</button>
            <button className="px-3 py-2 border rounded" onClick={() => setBgColor(bgColor === '#ffffff' ? '#fef9c3' : '#ffffff')}>🎨 T</button>
          </div>
  
          <textarea 
            name="responsable" 
            value={form.responsable} 
            onChange={handleChange} 
            className="w-full border p-3 rounded h-32" 
            style={{ 
              fontSize: fontSize + 'px', 
              backgroundColor: bgColor,
              direction: textDirection,
              fontWeight: fontWeight,
              fontStyle: fontStyle,
              textDecoration: textDecoration
            }}
          />
        </div>
  
        <div className="flex flex-wrap justify-end gap-3">
          <button type="reset" className="bg-red-300 text-white px-5 py-3 rounded hover:bg-red-400">Cancelar</button>
          <button type="button" onClick={() => alert('Datos aplicados')} className="bg-yellow-400 text-white px-5 py-3 rounded hover:bg-yellow-500">Aplicar</button>
          <button type="submit" onClick={(e) => { e.preventDefault(); alert('Datos guardados'); }} className="bg-green-500 text-white px-5 py-3 rounded hover:bg-green-600">Aceptar</button>
        </div>
      </div>
    );
  }