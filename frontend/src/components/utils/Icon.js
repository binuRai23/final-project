import Swal from "sweetalert2";

function Icon(icon, title, text) {
    const Icon = Swal.mixin({
        toast: true,
        position: "top",
        showConfirmButton: false,
        timer: 1500,
        timerProgressBar: true,
    });

    return Icon.fire({
        icon: icon,
        title: title,
        text: text,
    });
}

export default Icon;
