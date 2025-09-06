from django.db import models

# Create your models here.
productos = {
    "Chocolates": [
        {"nombre": "amargo", "descripción": "Chocolate con un alto contenido de cacao, con un sabor fuerte y un toque amargo.", "ingredientes principales": "Cacao, azúcar, manteca de cacao", "tiempo de producción/empaque": "2-3 días"},
        {"nombre": "con leche", "descripción": "Chocolate suave y cremoso, ideal para los amantes de los sabores dulces.", "ingredientes principales": "Leche en polvo, cacao, azúcar", "tiempo de producción/empaque": "1-2 días"},
        {"nombre": "con frutas deshidratadas", "descripción": "Chocolate con trozos de frutas secas que aportan un toque dulce y ácido.", "ingredientes principales": "Cacao, frutas deshidratadas, azúcar", "tiempo de producción/empaque": "3-4 días"},
        {"nombre": "blanco", "descripción": "Chocolate sin cacao en polvo, hecho con manteca de cacao, ideal para quienes buscan un sabor más suave.", "ingredientes principales": "Manteca de cacao, leche en polvo, azúcar", "tiempo de producción/empaque": "2-3 días"},
        {"nombre": "veganos", "descripción": "Chocolate libre de productos animales, ideal para personas veganas o con intolerancias.", "ingredientes principales": "Cacao, azúcar, leche de almendras", "tiempo de producción/empaque": "2-3 días"}
    ],
    "Galletas": [
        {"nombre": "avena", "descripción": "Galletas suaves y fibrosas, con el sabor característico de la avena.", "ingredientes principales": "Avena, azúcar, mantequilla", "tiempo de producción/empaque": "1-2 días"},
        {"nombre": "chocolate chip", "descripción": "Galletas crujientes con trozos de chocolate que se derriten al hornearlas.", "ingredientes principales": "Harina, azúcar, chocolate en trozos", "tiempo de producción/empaque": "1-2 días"},
        {"nombre": "rellenas de crema", "descripción": "Galletas con un relleno cremoso, generalmente de vainilla o chocolate.", "ingredientes principales": "Harina, azúcar, crema de chocolate", "tiempo de producción/empaque": "2-3 días"},
        {"nombre": "mantequilla", "descripción": "Galletas suaves, ricas en mantequilla, con un sabor dulce y delicado.", "ingredientes principales": "Harina, mantequilla, azúcar", "tiempo de producción/empaque": "1-2 días"},
        {"nombre": "jengibre", "descripción": "Galletas especiadas con jengibre, perfectas para el invierno o festividades.", "ingredientes principales": "Harina, azúcar, jengibre, canela", "tiempo de producción/empaque": "2-3 días"}
    ],
    "Alfajores": [
        {"nombre": "papaya", "descripción": "Alfajores rellenos de dulce de papaya, una versión tropical del tradicional.", "ingredientes principales": "Harina, azúcar, papaya, mantequilla", "tiempo de producción/empaque": "3-4 días"},
        {"nombre": "nuez", "descripción": "Alfajores rellenos de dulce de leche y decorados con nueces.", "ingredientes principales": "Harina, nuez, dulce de leche, manteca", "tiempo de producción/empaque": "3 días"},
        {"nombre": "chocolate negro", "descripción": "Alfajores cubiertos con chocolate amargo y rellenos de dulce de leche.", "ingredientes principales": "Harina, cacao, dulce de leche, chocolate amargo", "tiempo de producción/empaque": "3-4 días"},
        {"nombre": "sin azúcar", "descripción": "Alfajores aptos para personas con restricciones de azúcar, elaborados con edulcorantes.", "ingredientes principales": "Harina, edulcorante, mantequilla, dulce de leche sin azúcar", "tiempo de producción/empaque": "3-4 días"},
        {"nombre": "veganos", "descripción": "Alfajores sin ingredientes de origen animal, con relleno de dulce de leche vegano.", "ingredientes principales": "Harina, azúcar, aceite vegetal, dulce de leche vegano", "tiempo de producción/empaque": "3-4 días"}
    ],
    "Confitería": [
        {"nombre": "calugas de manjar de cabra", "descripción": "Dulces de manjar de cabra, suaves y cremosos, cubiertos con azúcar.", "ingredientes principales": "Manjar de cabra, azúcar, leche", "tiempo de producción/empaque": "1-2 días"},
        {"nombre": "cuchuflí de chocolate", "descripción": "Rollos crujientes rellenos de crema de chocolate y cubiertos de chocolate amargo.", "ingredientes principales": "Harina, azúcar, chocolate, crema", "tiempo de producción/empaque": "2 días"},
        {"nombre": "gomitas", "descripción": "Gomitas de diferentes sabores, ideales para un toque de dulzura y textura gomosa.", "ingredientes principales": "Gelatina, azúcar, saborizantes artificiales", "tiempo de producción/empaque": "1-2 días"},
        {"nombre": "vitaminizadas", "descripción": "Gomitas con vitaminas añadidas, combinando dulzura con beneficios para la salud.", "ingredientes principales": "Gelatina, azúcar, vitaminas", "tiempo de producción/empaque": "1-2 días"},
        {"nombre": "entre otros", "descripción": "Variedad de productos confiteros que incluyen caramelos, chicles y más.", "ingredientes principales": "Azúcar, gelatina, sabores artificiales", "tiempo de producción/empaque": "2 días"}
    ],
    "Bombonería": [
        {"nombre": "trufa", "descripción": "Bombones rellenos de una mezcla suave y rica de chocolate y crema.", "ingredientes principales": "Cacao, crema, azúcar", "tiempo de producción/empaque": "2-3 días"},
        {"nombre": "licor", "descripción": "Bombones rellenos de licor, generalmente whisky, ron o licor de cereza.", "ingredientes principales": "Cacao, licor, azúcar", "tiempo de producción/empaque": "2-3 días"},
        {"nombre": "frutas", "descripción": "Bombones con rellenos de frutas, como naranja, frambuesa o cereza.", "ingredientes principales": "Cacao, frutas, azúcar", "tiempo de producción/empaque": "2-3 días"},
        {"nombre": "praline", "descripción": "Bombones rellenos de una mezcla de azúcar caramelizado y frutos secos, generalmente avellanas.", "ingredientes principales": "Cacao, avellanas, azúcar", "tiempo de producción/empaque": "2-3 días"},
        {"nombre": "chocolate blanco relleno", "descripción": "Bombones de chocolate blanco rellenos de cremas suaves o frutas.", "ingredientes principales": "Manteca de cacao, leche, azúcar, frutas", "tiempo de producción/empaque": "2-3 días"}
    ]
}
