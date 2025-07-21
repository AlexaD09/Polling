
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
const IP_BACKEND = window.location.hostname;
//Carga el reporte cobinado del microservicio Resporteservice
async function cargarReporteCombinado() { 
  const resp = await fetch(`http://${IP_BACKEND}:8003/api/reporte/combinado`);
  const data = await resp.json();//obtiene los datos en formatos json
  console.log("Datos completos recibidos:", data);  //  imprimir todo
  const resumen_estado = generarResumenEstados(data); //generar un resumen por estado
  const tbody = document.querySelector("#tablaCombinada tbody");
  tbody.innerHTML = "";// limpia contenido previo

  //Llena la tabla con los datos recibidos
  data.forEach(q => {
    const row = `<tr>
      <td>${q.origen}</td><td>${q.nombre}</td>
      <td>${q.correo}</td><td>${q.titulo}<br>${q.descripcion}</td>
      <td>${q.estado}</td>
    </tr>`;
    tbody.innerHTML += row;
  });

  generarGrafica(resumen_estado); //Dibuja una grafica con los etados  
}

//Funcion para cargar las recomendacines generadas con ia
async function mostrarRecomendaciones() {
  const resp = await fetch(`http://${IP_BACKEND}:8003/api/recomendaciones`);
  const data = await resp.json();//Obtiene la recomendacion
  alert("Recomendación: " + data.recomendacion);// muestra una alestra con la recomendacion
}

//Funcion que genera la grafica con el resumen que tenemos despues de cargar el dto combinado

function generarGrafica(resumen) {
  const ctx = document.getElementById("graficoQuejas").getContext("2d");
  new Chart(ctx, {
 
    type: "bar",
    data: {
      labels: Object.keys(resumen),
      
      datasets: [{
        label: "Cantidad por estado",
        data: Object.values(resumen),
        backgroundColor: ["#2ecc71","#3498db", "#e74c3c"]
      }]
    }
  });
}

// Convertimos en los datos aceptados para poder generar la grafica

function generarResumenEstados(quejas) {
  const resumen = {};
  quejas.forEach(q => {
    let estado = q.estado || "Desconocido";
    estado = estado.trim().toLowerCase(); // Limpia espacios y convierte a minúscula
    estado = estado.charAt(0).toUpperCase() + estado.slice(1); // Primera letra mayúscula

    resumen[estado] = (resumen[estado] || 0) + 1;
  });
  return resumen;
}

//Funcion para Guardar los empleados en nuestra bd de usuarios.

document.getElementById("registroEmpleadoForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  // Obtiene datos del formulario
  const nombre = document.getElementById("nombreEmpleado").value.trim();
  const correo = document.getElementById("correoEmpleado").value.trim();

  // Valida campos
  if (!nombre || !correo) {
    alert("Completa todos los campos");
    return;
  }

  // Datos fijos para empleados
  const data = {
    nombre,
    correo,
    pssw: "empleado",  // fija la contraseña aquí
    rol: "empleado"          // fija el rol aquí
  };

  console.log("Enviando:", data);


  try {
    // Envía los datos al backend
    const res = await fetch(`http://${IP_BACKEND}:8000/usuarios/registro`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Error al registrar empleado");
    alert("Empleado registrado correctamente");
    document.getElementById("registroEmpleadoForm").reset();
    
  } catch (err) {
    alert("Error al registrar empleado");
    console.error(err);
  }
});

// Cargar las quejas web
async function cargarQuejasWeb() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  try {
    const res = await fetch(`http://${IP_BACKEND}:8003/api/reporte/web`, {
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
        
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("❌ Error al cargar quejas web:", err);
  }
}

//Cargar quejas de oficina
async function cargarQuejasOficina() {
  const token = localStorage.getItem("access_token");
  if (!token) return;
  const decoded = parseJwt(token);
    try{
     const res = await fetch(`http://${IP_BACKEND}:8003/api/reporte/oficina`,{
       headers: {
         "Authorization": `Bearer ${token}`
     }
  });


  if (!res.ok) throw new Error("No se pudieron cargar las quejas");

  const quejas = await res.json();

  console.log("📦 Quejas recibidas:", quejas); // 👈 Ver si llega
  const tbody = document.querySelector("#tablaQuejasOficina tbody");
  tbody.innerHTML = "";

   quejas.forEach(q => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${q.id_queja}</td>
      <td>${q.nombre_cliente}</td>
      <td>${q.correo_cliente}</td>
      <td>${q.titulo}</td>
      <td>${q.descripcion}</td>
      <td>${q.estado}</td>
      
    `;
    tbody.appendChild(tr);
  });

}catch (err) {
    console.error("❌ Error al cargar quejas:", err);
  }  
}

//Cargar usuarios

async function cargarUsuarios() {
  try {
    const res = await fetch(`http://${IP_BACKEND}:8000/usuarios/usuarios`);
    if (!res.ok) throw new Error("Error al cargar los usuarios");
    const usuarios = await res.json();

    console.log("👤 Usuarios recibidos:", usuarios);

    const tbody = document.querySelector("#tablaUsuarios tbody");
    tbody.innerHTML = "";

    usuarios.forEach(u => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${u.nombre}</td>
        <td>${u.correo}</td>
        <td>${u.rol}</td>
      `;
      tbody.appendChild(tr);
    });

  } catch (err) {
    console.error("❌ Error al cargar usuarios:", err);
  }
}



// Evento para cerrar sesión
document.getElementById("btnLogout").addEventListener("click", function () {
  localStorage.removeItem("access_token");
  console.log("🔐 Token eliminado. Cerrando sesión...");
  window.location.href = "/index.html";  // Redirige al login o página de inicio
});

window.onload = () => {
  cargarQuejasOficina();
  cargarQuejasWeb();
  cargarUsuarios(); // si también lo tienes
};

document.addEventListener("DOMContentLoaded", cargarReporteCombinado);
