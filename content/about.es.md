---
title: "Sobre Romain Charretteur"
description: "Conoce a Romain Charretteur, desarrollador de software y fotógrafo de viajes radicado en Montreal, explorando el mundo a través de su lente."
layout: "simple"
showReadingTime: false
showDate: false
showAuthor: false
showComments: false
---

<div class="about-container">
<div class="main-layout" style="display: flex; gap: 50px; align-items: center; min-height: 500px;">

<div class="sidebar" style="flex: 0 0 300px;">
<img src="/about.jpeg" alt="Romain Charretteur" style="width: 100%; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
</div>

<div class="content-area" style="flex: 1;">

<div class="profile-description" style="margin-bottom: 1rem;">
<p style="font-size: 1.1rem; line-height: 1.7; margin-bottom: 1rem;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Nacido en 1995 en Brest (Francia), soy un desarrollador de software que vive actualmente en Montreal.</p>
<p style="font-size: 1.1rem; line-height: 1.7;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Empecé la fotografía como afición tras mudarme a Canadá. Utilizo este sitio para compartir mis fotos de viajes por Europa y Norteamérica, centrándome en la arquitectura de las ciudades y los paisajes naturales.</p>
</div>

<div class="gear-sub-section" style="display: flex; align-items: center; gap: 30px; padding: 0;">

<div class="gear-text" style="flex: 1;">
<h3 style="margin-bottom: 1rem; font-size: 1.3rem; letter-spacing: 1px;">Equipo</h3>
<ul style="list-style: none; padding: 0; line-height: 1.8; font-size: 0.95rem;">
<li><strong>Cámara:</strong> Sony Alpha 6700 + Sigma 18-50mm f/2.8</li>
<li><strong>Dron:</strong> DJI Mini 5 Pro</li>
<li><strong>Móvil:</strong> iPhone 17</li>
</ul>
</div>

<div class="gear-visual" style="flex: 1.5; position: relative; height: 200px; min-width: 250px;">
<img src="/drone.png" class="gear-img img-drone" alt="Dron">
<img src="/objectif.png" class="gear-img img-lens" alt="Lente">
<img src="/sony.png" class="gear-img img-camera" alt="Sony">
</div>

</div>
</div>
</div>
</div>

<style>
/* Style Desktop par défaut */
.gear-img { position: absolute; filter: drop-shadow(0 6px 10px rgba(0,0,0,0.15)); }
.img-drone { width: 110px; top: 0; left: 50%; transform: translateX(-50%); z-index: 3; }
.img-lens { width: 65px; bottom: 5px; left: 10%; transform: rotate(-10deg); z-index: 2; }
.img-camera { width: 90px; bottom: 10px; right: 10%; transform: rotate(5deg); z-index: 2; }

@media (max-width: 900px) {
    .main-layout { flex-direction: column !important; text-align: center; }
    .sidebar { flex: none !important; width: 100% !important; max-width: 250px; }
    .gear-sub-section { flex-direction: column !important; gap: 20px !important; }
    
    .gear-visual { 
        height: auto !important; 
        display: flex !important; 
        justify-content: center !important; 
        align-items: center !important;
        gap: 15px !important;
        position: static !important; 
    }
    .gear-img { 
        position: static !important; 
        transform: none !important; 
        width: 80px !important; 
        height: auto !important;
    }
}
</style>