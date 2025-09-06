from django.db import models

# Create your models here.
productos = {
    "Chocolates": [
        {"nombre": "amargo", "descripción": "Chocolate con un alto contenido de cacao, con un sabor fuerte y un toque amargo.", "ingredientes_principales": "Cacao, azúcar, manteca de cacao", "tiempo_de_producción_empaque": "2-3 días"},
        {"nombre": "con leche", "descripción": "Chocolate suave y cremoso, ideal para los amantes de los sabores dulces.", "ingredientes_principales": "Leche en polvo, cacao, azúcar", "tiempo_de_producción_empaque": "1-2 días"},
        {"nombre": "con frutas deshidratadas", "descripción": "Chocolate con trozos de frutas secas que aportan un toque dulce y ácido.", "ingredientes_principales": "Cacao, frutas deshidratadas, azúcar", "tiempo_de_producción_empaque": "3-4 días"},
        {"nombre": "blanco", "descripción": "Chocolate sin cacao en polvo, hecho con manteca de cacao, ideal para quienes buscan un sabor más suave.", "ingredientes_principales": "Manteca de cacao, leche en polvo, azúcar", "tiempo_de_producción_empaque": "2-3 días"},
        {"nombre": "veganos", "descripción": "Chocolate libre de productos animales, ideal para personas veganas o con intolerancias.", "ingredientes_principales": "Cacao, azúcar, leche de almendras", "tiempo_de_producción_empaque": "2-3 días"}
    ],
    "Galletas": [
        {"nombre": "avena", "descripción": "Galletas suaves y fibrosas, con el sabor característico de la avena.", "ingredientes_principales": "Avena, azúcar, mantequilla", "tiempo_de_producción_empaque": "1-2 días"},
        {"nombre": "chocolate chip", "descripción": "Galletas crujientes con trozos de chocolate que se derriten al hornearlas.", "ingredientes_principales": "Harina, azúcar, chocolate en trozos", "tiempo_de_producción_empaque": "1-2 días"},
        {"nombre": "rellenas de crema", "descripción": "Galletas con un relleno cremoso, generalmente de vainilla o chocolate.", "ingredientes_principales": "Harina, azúcar, crema de chocolate", "tiempo_de_producción_empaque": "2-3 días"},
        {"nombre": "mantequilla", "descripción": "Galletas suaves, ricas en mantequilla, con un sabor dulce y delicado.", "ingredientes_principales": "Harina, mantequilla, azúcar", "tiempo_de_producción_empaque": "1-2 días"},
        {"nombre": "jengibre", "descripción": "Galletas especiadas con jengibre, perfectas para el invierno o festividades.", "ingredientes_principales": "Harina, azúcar, jengibre, canela", "tiempo_de_producción_empaque": "2-3 días"}
    ],
    "Alfajores": [
        {"nombre": "papaya", "descripción": "Alfajores rellenos de dulce de papaya, una versión tropical del tradicional.", "ingredientes_principales": "Harina, azúcar, papaya, mantequilla", "tiempo_de_producción_empaque": "3-4 días"},
        {"nombre": "nuez", "descripción": "Alfajores rellenos de dulce de leche y decorados con nueces.", "ingredientes_principales": "Harina, nuez, dulce de leche, manteca", "tiempo_de_producción_empaque": "3 días"},
        {"nombre": "chocolate negro", "descripción": "Alfajores cubiertos con chocolate amargo y rellenos de dulce de leche.", "ingredientes_principales": "Harina, cacao, dulce de leche, chocolate amargo", "tiempo_de_producción_empaque": "3-4 días"},
        {"nombre": "sin azúcar", "descripción": "Alfajores aptos para personas con restricciones de azúcar, elaborados con edulcorantes.", "ingredientes_principales": "Harina, edulcorante, mantequilla, dulce de leche sin azúcar", "tiempo_de_producción_empaque": "3-4 días"},
        {"nombre": "para veganos", "descripción": "Alfajores sin ingredientes de origen animal, con relleno de dulce de leche vegano.", "ingredientes_principales": "Harina, azúcar, aceite vegetal, dulce de leche vegano", "tiempo_de_producción_empaque": "3-4 días"}
    ],
    "Confitería": [
        {"nombre": "calugas de manjar de cabra", "descripción": "Dulces de manjar de cabra, suaves y cremosos, cubiertos con azúcar.", "ingredientes_principales": "Manjar de cabra, azúcar, leche", "tiempo_de_producción_empaque": "1-2 días"},
        {"nombre": "cuchuflí de chocolate", "descripción": "Rollos crujientes rellenos de crema de chocolate y cubiertos de chocolate amargo.", "ingredientes_principales": "Harina, azúcar, chocolate, crema", "tiempo_de_producción_empaque": "2 días"},
        {"nombre": "gomitas", "descripción": "Gomitas de diferentes sabores, ideales para un toque de dulzura y textura gomosa.", "ingredientes_principales": "Gelatina, azúcar, saborizantes artificiales", "tiempo_de_producción_empaque": "1-2 días"},
        {"nombre": "vitaminizadas", "descripción": "Gomitas con vitaminas añadidas, combinando dulzura con beneficios para la salud.", "ingredientes_principales": "Gelatina, azúcar, vitaminas", "tiempo_de_producción_empaque": "1-2 días"},
        {"nombre": "entre otros", "descripción": "Variedad de productos confiteros que incluyen caramelos, chicles y más.", "ingredientes_principales": "Azúcar, gelatina, sabores artificiales", "tiempo_de_producción_empaque": "2 días"}
    ],
    "Bombonería": [
        {"nombre": "trufa", "descripción": "Bombones rellenos de una mezcla suave y rica de chocolate y crema.", "ingredientes_principales": "Cacao, crema, azúcar", "tiempo_de_producción_empaque": "2-3 días"},
        {"nombre": "licor", "descripción": "Bombones rellenos de licor, generalmente whisky, ron o licor de cereza.", "ingredientes_principales": "Cacao, licor, azúcar", "tiempo_de_producción_empaque": "2-3 días"},
        {"nombre": "frutas", "descripción": "Bombones con rellenos de frutas, como naranja, frambuesa o cereza.", "ingredientes_principales": "Cacao, frutas, azúcar", "tiempo_de_producción_empaque": "2-3 días"},
        {"nombre": "praline", "descripción": "Bombones rellenos de una mezcla de azúcar caramelizado y frutos secos, generalmente avellanas.", "ingredientes_principales": "Cacao, avellanas, azúcar", "tiempo_de_producción_empaque": "2-3 días"},
        {"nombre": "chocolate blanco relleno", "descripción": "Bombones de chocolate blanco rellenos de cremas suaves o frutas.", "ingredientes_principales": "Manteca de cacao, leche, azúcar, frutas", "tiempo_de_producción_empaque": "2-3 días"}
    ]
}

