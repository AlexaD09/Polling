//usuarioservice
document.getElementById("loginForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const correo = document.getElementById("correo").value;
  const contraseña = document.getElementById("contraseña").value;

  const res = await fetch("http://localhost:8000/usuarios/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ correo, contraseña })
  });

  const data = await res.json();

  if (res.ok) {
    localStorage.setItem("token", data.access_token);
    window.location.href = "/cliente.html";
  } else {
    document.getElementById("mensaje").innerText = "Credenciales incorrectas";
  }
});
