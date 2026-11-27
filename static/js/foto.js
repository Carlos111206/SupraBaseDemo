// Muestra una vista previa de la foto elegida antes de enviar el formulario
document.addEventListener("DOMContentLoaded", () => {
  const entrada = document.getElementById("foto");
  const vista = document.getElementById("vista-previa");
  if (!entrada || !vista) return;
  entrada.addEventListener("change", () => {
    const archivo = entrada.files && entrada.files[0];
    if (archivo) vista.src = URL.createObjectURL(archivo);
  });
});
