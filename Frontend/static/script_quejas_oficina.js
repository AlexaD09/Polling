// Función para decodificar JWT 
function parseJwt(token) {
  if (!token) return null;
  const base64Url = token.split('.')[1];
  if (!base64Url) return null;
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split('')
      .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
  );
  return JSON.parse(jsonPayload);
}

//Funcion para enviar nueva queja.
async function enviarQueja() {
  //Obtiene los valores del formulario
  const nombre= document.getElementById("nombre").value.trim();
  const correo = document.getElementById("correo").value.trim();
  const titulo = document.getElementById("tituloQueja").value.trim();
  const descripcion = document.getElementById("descripcion").value.trim();
  //verifica si hay un token de sesion
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    alert("Debes iniciar sesión para enviar una queja.");
    window.location.href = "/index.html";
    return;
  }

  //valida que todos los campos esten completos
  if (!nombre || !correo || !titulo || !descripcion) {
    alert("Completa todos los campos");
    return;
  }

   //decodifica el token para obtener datos como el id de usuario
  const decodedToken = parseJwt(token);  
  const id_usuario = decodedToken.sub;

  //Crea el objeto con los datos de la nueva queja
  const nuevaQueja = {
    id_usuario: id_usuario,
    nombre_cliente: nombre ,
    correo_cliente: correo,
    titulo: titulo,
    descripcion: descripcion
  };

  //Muestra los datos que se van a enviar
  console.log("Enviando queja:", nuevaQueja);
  console.log("Token:", token);

  try {
    //Envia la queja al backend
    const res = await fetch("http://localhost:8002/oficina/quejas-oficina/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(nuevaQueja)
    });

    if (!res.ok) throw new Error(`Error HTTP: ${res.status}`);

    alert("Queja registrada correctamente.");

    //  Limpiar todos los campos del formulario
    document.getElementById("formQueja").reset();  // 👈 Esto sí funciona si apuntas bien al form

  } catch (error) {
    console.error("Error al registrar queja:", error);
    alert("No se pudo registrar la queja. Revisa la consola.");
  }
}

console.log("👀 Ejecutando cargarQuejasOficina...");
//Cargar las quejas de la oficina desde el backend
async function cargarQuejasOficina() {
  const token = localStorage.getItem("access_token");
  if (!token) return;
  const decoded = parseJwt(token);
    try{
      //Obtiene las quejas desde el backend
     const res = await fetch("http://localhost:8003/api/reporte/oficina",{
       headers: {
         "Authorization": `Bearer ${token}`
     }
  });


  if (!res.ok) throw new Error("No se pudieron cargar las quejas");

  const quejas = await res.json(); //Convierte la respuesta a json

  console.log("📦 Quejas recibidas:", quejas); // 👈 Ver si llega
  const tbody = document.querySelector("#tablaQuejasOficina tbody");
  tbody.innerHTML = ""; //limpiar toda la tabla

  //Crear una fila por cada queja
   quejas.forEach(q => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${q.id_queja}</td>
      <td>${q.nombre_cliente}</td>
      <td>${q.correo_cliente}</td>
      <td>${q.titulo}</td>
      <td>${q.descripcion}</td>
      <td>${q.estado}</td>
      <td>
         <select class="form-select form-select-sm" onchange="cambiarEstadoOficina(${q.id_queja}, this.value)">
        <option value="Pendiente" ${q.estado === 'Pendiente' ? 'selected' : ''}>Pendiente</option>
        <option value="En proceso" ${q.estado === 'En proceso' ? 'selected' : ''}>En proceso</option>
        <option value="Resuelto" ${q.estado === 'Resuelto' ? 'selected' : ''}>Resuelto</option>
      </select>
      </td>
    `;
    tbody.appendChild(tr);
  });

}catch (err) {
    console.error("❌ Error al cargar quejas:", err);
  }  
}

// Evento para cerrar sesión
document.getElementById("btnLogout").addEventListener("click", function () {
  localStorage.removeItem("access_token"); //Elimina el token
  console.log("🔐 Token eliminado. Cerrando sesión...");
  window.location.href = "/index.html";  // Redirige al login o página de inicio
});


document.getElementById("formQueja").addEventListener("submit", function (e) {
  e.preventDefault();//Evita recargar la pagina
  enviarQueja().then(cargarQuejasOficina); // envia la queja y recarga la tabla
});

//Funcion para cambiar el estado de la accion
async function cambiarEstadoOficina(id_queja, nuevoEstado) {
   console.log("ID queja a cambiar:", id_queja);
  const token = localStorage.getItem("access_token");
  if (!token) return;
 
  try {
    //Envia la actualizacion la backend
    const res = await fetch(`http://localhost:8002/oficina/quejas-oficina/${id_queja}/estado?nuevo_estado=${nuevoEstado}`, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) throw new Error("No se pudo cambiar el estado");

    alert("Estado actualizado correctamente.");
    await cargarQuejasOficina();  // 👈 Recarga la tabla

  } catch (error) {
    console.error("❌ Error al cambiar estado:", error);
    alert("Ocurrió un error al actualizar el estado.");
  }
}

//Funcion cargar quejas web
async function cargarQuejasWeb() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  try {
    const res = await fetch("http://localhost:8003/api/reporte/web", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) throw new Error("No se pudieron cargar las quejas web");

    const quejas = await res.json();
    const tbody = document.querySelector("#tablaQuejasWeb tbody");
    tbody.innerHTML = "";

    quejas.forEach(q => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${q.id}</td>
        <td>${q.nombre}</td>
        <td>${q.email}</td>
        <td>${q.titulo}</td>
        <td>${q.descripcion}</td>
        <td>${q.estado}</td>
        <td>
          <select onchange="cambiarEstadoWeb('${q.id}', this.value)" class="form-select form-select-sm">
            <option value="Pendiente" ${q.estado === "Pendiente" ? "selected" : ""}>Pendiente</option>
            <option value="En Proceso" ${q.estado === "En Proceso" ? "selected" : ""}>En Proceso</option>
            <option value="Resuelto" ${q.estado === "Resuelto" ? "selected" : ""}>Resuelto</option>
          </select>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("❌ Error al cargar quejas web:", err);
  }
}

//Funcion para cambiar el estado de la queja web
async function cambiarEstadoWeb(id, nuevoEstado) {
  const token = localStorage.getItem("access_token");

  try {
    const res = await fetch(`http://localhost:8001/quejas-web/${id}/estado?nuevo_estado=${nuevoEstado}`, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!res.ok) throw new Error("No se pudo actualizar el estado");

    alert("Estado actualizado correctamente.");
    cargarQuejasWeb();

  } catch (err) {
    console.error("❌ Error al cambiar estado:", err);
  }
}

window.onload = () => {
  cargarQuejasOficina();//carga las quejas de oficina
  cargarQuejasWeb(); // carga las quejas del sitio web
};