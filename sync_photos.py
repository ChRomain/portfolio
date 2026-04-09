import os
import re
import shutil
from PIL import Image, ImageOps
import piexif

SOURCE_DIR = "/Users/romaincharretteur/pCloud Drive/Portfolio_Images"
CONTENT_DIR = "./content/gallery"
ASSETS_DIR = "./static/gallery" 

# --- PARAMÈTRES D'OPTIMISATION ---
QUALITY = 55          # Qualité WebP
MAX_WIDTH = 1600      # Largeur max

# --- BASE DE DONNÉES VIDÉOS ---
VIDEOS = {
    "new_york": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-06%2023-47-51.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-08%2012-20-58.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-06-23%2013-16-26.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-06%2000-27-10.mov"
    ],
    "finistere": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-05-21%2017-30-11.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-19%2014-54-12.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-19%2014-53-02.mp4"
    ],
    "new_hampshire": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-10-06%2011-54-14.mov"
    ],
    "montreal": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-07-07%2000-04-23.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-07-09%2021-46-58.mov"
    ],
    "niagara_falls": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-08-24%2010-38-55.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-08-24%2013-22-45.mp4"
    ],
    "quebec": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-10-14%2000-31-25.mov"
    ],
    "canada": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-07-08%2023-38-40.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-02-11%2014-29-22.mov"
    ],
    "guatemala": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-09-10%2014-31-25.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-01-23%2010-52-09.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-09-03%2008-48-03.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-09-11%2019-05-15.mov"
    ],
    "keys": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-07%2019-10-13.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-07%2023-15-36.mp4"
    ],
    "miami": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-07-17.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-08-17.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-06-15.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-05%2020-26-44.mov"
    ],
    "everglades": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-09-58.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-12-38.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-13-27.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-14-12.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-14-59.mov"
    ]
}

DESCRIPTIONS = {
    "indonesie": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Between ancestral temples, secret Balinese beaches, volcanic mists, and lush jungles, dive into a visual exploration of Indonesian contrasts—where wild nature meets sacred serenity.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Entre temples ancestraux, plages secrètes de Bali, brumes volcaniques et jungles luxuriantes, plongez dans une exploration visuelle des contrastes indonésiens—où la nature sauvage rencontre la sérénité sacrée.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Entre templos ancestrales, playas secretas de Bali, brumas volcánicas y selvas exuberantes, sumérgete en una exploración visual de los contrastes indonesios, donde la naturaleza salvaje se encuentra con la serenidad sagrada."
    },
    "guatemala": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;From the cobblestone streets of Antigua and ancient Mayan pyramids to the fiery peaks of Fuego and Acatenango, embark on a visual journey through Guatemala's timeless soul—where colonial history meets the raw power of the earth.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Des rues pavées d'Antigua et des anciennes pyramides mayas aux sommets enflammés du Fuego et de l'Acatenango, embarquez pour un voyage visuel à travers l'âme intemporelle du Guatemala—où l'histoire coloniale rencontre la puissance brute de la terre.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Desde las calles empedradas de Antigua y las antiguas pirámides mayas hasta los picos ardientes de Fuego y Acatenango, embárcate en un viaje visual a través del alma atemporal de Guatemala, donde la historia colonial se encuentra con el poder puro de la tierra."
    },
    "cape_cod": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;From iconic lighthouses guarding the vast Atlantic to the serene dance of whales on the horizon, discover the soulful charm of Cape Cod. A captivating journey through New England's coastal landscapes, where peaceful shores meet maritime history.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Des phares emblématiques gardant le vaste Atlantique à la danse sereine des baleines à l'horizon, découvrez le charme émouvant de Cape Cod. Un voyage captivant à travers les paysages couteaux de la Nouvelle-Angleterre, où les rivages paisibles rencontrent l'histoire maritime.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Desde los faros icónicos que custodian el vasto Atlántico hasta la danza serena de las ballenas en el horizonte, descubre el encanto conmovedor de Cape Cod. Un viaje cautivador a través de los paisajes costeros de Nueva Inglaterra, donde las orillas pacíficas se encuentran con la historia marítima."
    },
    "vermont": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Immerse yourself in the tranquil beauty of the Green Mountain State. From the serene shores of Lake Willoughby to the lush, rolling hills that define the landscape, witness a peaceful harmony where nature takes center stage.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Immergez-vous dans la beauté tranquille de l'État des Montagnes Vertes. Des rives sereines du lac Willoughby aux collines luxuriantes qui définissent le paysage, témoignez d'une harmonie paisible où la nature occupe le devant de la scène.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Sumérgete en la belleza tranquila del Estado de las Montañas Verdes. Desde las orillas serenas del lago Willoughby hasta las colinas exuberantes que definen el paisaje, presencia una armonía pacífica donde la naturaleza toma el protagonismo."
    },
    "new_hampshire": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Experience the fleeting magic of the Indian Summer. From the fiery foliage of the White Mountains to the golden-hued winding roads of the Kancamagus Highway, lose yourself in a landscape painted in nature’s most vibrant autumn tones.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Découvrez la magie fugace de l'été indien. Du feuillage flamboyant des Montagnes Blanches aux routes sinueuses aux teintes dorées de la route Kancamagus, perdez-vous dans un paysage peint aux tons d'automne les plus vibrants de la nature.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Experimenta la magia fugaz del verano indio. Desde el follaje ardiente de las Montañas Blancas hasta las carreteras sinuosas de tonos dorados de la autopista Kancamagus, piérdete en un paisaje pintado con los tonos otoñales más vibrantes de la naturaleza."
    },
    "washington": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Walk through the heart of American history. From the neoclassical grandeur of the White House and the Capitol at night to the red towers of the Smithsonian, witness a city where every corner tells a story of power and heritage.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Marchez au cœur de l'histoire américaine. De la grandeur néoclassique de la Maison Blanche et du Capitole la nuit aux tours rouges du Smithsonian, témoignez d'une ville où chaque coin raconte une histoire de pouvoir et d'héritage.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Camina por el corazón de la historia estadounidense. Desde la grandeza neoclásica de la Casa Blanca y el Capitolio por la noche hasta las torres rojas del Smithsonian, presencia una ciudad donde cada rincón cuenta una historia de poder y herencia."
    },
    "suede": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Step into a Nordic winter wonderland. From the glowing reindeer displays and festive city lights to the serene, frozen harbors, experience the enchanting magic of a Swedish winter where the darkness of the season is met with a warm, golden glow.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Entrez dans un pays des merveilles hivernal nordique. Des rennes lumineux et des lumières festives de la ville aux ports sereins et gelés, découvrez la magie enchanteresse d'un hiver suédois où l'obscurité de la saison rencontre une lueur chaude et dorée.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Entra en un país de las maravillas invernal nórdico. Desde las exhibiciones de renos brillantes y las luces festivas de la ciudad hasta los puertos serenos y congelados, experimenta la magia encantadora de un invierno sueco donde la oscuridad de la temporada se encuentra con un brillo cálido y dorado."
    },
    "toronto": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Rising above the shores of Lake Ontario, experience the vibrant pulse of Canada's largest metropolis. From the dizzying heights of the CN Tower to the bustling streets of downtown, witness a city where soaring glass towers meet a rich, multicultural heart.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;S'élevant au-dessus des rives du lac Ontario, découvrez le pouls vibrant de la plus grande métropole du Canada. Des hauteurs vertigineuses de la Tour CN aux rues animées du centre-ville, témoignez d'une ville où les tours de verre vertigineuses rencontrent un cœur riche et multiculturel.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Elevándose sobre las orillas del lago Ontario, experimenta el pulso vibrante de la metrópolis más grande de Canadá. Desde las alturas vertiginosas de la Torre CN hasta las calles bulliciosas del centro, presencia una ciudad donde las torres de vidrio se encuentran con un corazón rico y multicultural."
    },
    "rome": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Step back through two thousand years of history. From the colossal heights of the Colosseum to the moonlit elegance of the Trevi Fountain and the Pantheon, witness a city where the ancient world and modern life breathe as one.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Reculez de deux mille ans dans l'histoire. Des hauteurs colossales du Colisée à l'élégance au clair de lune de la fontaine de Trevi et du Panthéon, témoignez d'une ville où le monde antique et la vie moderne ne font qu'un.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Retrocede dos mil años en la historia. Desde las alturas colosales del Coliseo hasta la elegancia a la luz de la luna de la Fontana de Trevi y el Panteón, presencia una ciudad donde el mundo antiguo y la vida moderna respiran como uno solo."
    },
    "naples": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;In the shadow of Mount Vesuvius, experience the raw and captivating soul of Southern Italy. Journey through a city where ancient history and vibrant street life collide under a Mediterranean sun that turns every crumbling facade into a golden masterpiece.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;À l'ombre du Vésuve, découvrez l'âme brute et captivante de l'Italie du Sud. Voyagez à travers une ville où l'histoire ancienne et la vie de rue vibrante se heurtent sous un soleil méditerranéen qui transforme chaque façade en ruine en un chef-d'œuvre doré.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;A la sombra del Monte Vesubio, experimenta el alma cruda y cautivadora del sur de Italia. Viaja a través de una ciudad donde la historia antigua y la vibrante vida callejera chocan bajo un sol mediterráneo que convierte cada fachada desmoronada en una obra maestra dorada."
    },
    "paris": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Experience the timeless allure of the City of Light. From the sparkling iron lattice of the Eiffel Tower at night to the bohemian glow of Montmartre and the red velvet charm of the Moulin Rouge, witness a city that never loses its romantic spark.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Découvrez l'attrait intemporel de la Ville Lumière. Du treillis de fer scintillant de la Tour Eiffel la nuit à la lueur bohème de Montmartre et au charme de velours rouge du Moulin Rouge, témoignez d'une ville qui ne perd jamais son étincelle romantique.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Experimenta el encanto atemporal de la Ciudad de la Luz. Desde la brillante celosía de hierro de la Torre Eiffel por la noche hasta el resplandor bohemio de Montmartre y el encanto de terciopelo rojo del Moulin Rouge, presencia una ciudad que nunca pierde su chispa romántica."
    },
    "lyon": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Traverse the layers of time in France’s gastronomic capital. From the shimmering mosaics of the Fourvière Basilica to the secret Renaissance courtyards of the Old Town, uncover a city where architectural grandeur and hidden history gracefully intertwine.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Traversez les couches du temps dans la capitale gastronomique de la France. Des mosaïques scintillantes de la basilique de Fourvière aux cours secrètes de la Renaissance du Vieux Lyon, découvrez une ville où la grandeur architecturale et l'histoire cachée s'entremêlent gracieusement.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Atraviesa las capas del tiempo en la capital gastronomique de Francia. Desde los mosaicos brillantes de la Basílica de Fourvière hasta los patios secretos del Renacimiento en el casco antiguo, descubre una ciudad donde la grandeur architecturale et l'histoire cachée s'entremêlent gracieusement."
    },
    "bordeaux": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplate a city where history and modernity find a perfect balance. From the golden stone of the Grosse Cloche to the futuristic curves of the Cité du Vin, embark on an odyssey through Bordeaux’s grand boulevards and its hidden, vibrant street-art sanctuaries.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplez une ville où l'histoire et la modernité trouvent un équilibre parfait. De la pierre dorée de la Grosse Cloche aux courbes futuristes de la Cité du Vin, embarquez pour une odyssée à travers les grands boulevards de Bordeaux et ses sanctuaires cachés et vibrants de street-art.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Contempla una ciudad donde la historia y la modernidad encuentran un equilibrio perfecto. Desde la piedra dorada de la Grosse Cloche hasta las curvas futuristas de la Cité du Vin, embárcate en una odisea a través de los grandes bulevares de Bordeaux y sus santuarios de arte callejero ocultos y vibrantes."
    },
    "finistere": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplate the raw majesty of the 'Land's End'. From the legendary lighthouses of Saint-Mathieu guarding the rugged cliffs to the turquoise waters of hidden coves, embark on a visual journey through Brittany’s untamed coastline where the Atlantic meets the soul of the earth.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplez la majesté brute du 'Bout du Monde'. Des phares légendaires de Saint-Mathieu gardant les falaises escarpées aux eaux turquoise des criques cachées, embarquez pour un voyage visuel à travers le littoral sauvage de la Bretagne où l'Atlantique rencontre l'âme de la terre.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Contempla la majestuosidad cruda del 'Fin de la Tierra'. Desde los faros legendarios de Saint-Mathieu que custodian los acantilados escarpados hasta las aguas turquesas de calas ocultas, embárcate en un voyage visual a través de la costa indómita de Bretaña, donde el Atlántico se encuentra con el alma de la tierra."
    },
    "boston": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Trace the footsteps of history along the cobblestone paths of Beacon Hill. From the grandeur of Quincy Market to the historic docks of the harbor, encounter a city where the spirit of American independence lives on through every brick and monument.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Retracez les pas de l'histoire le long des sentiers pavés de Beacon Hill. De la grandeur du marché Quincy aux quais historiques du port, rencontrez une ville où l'esprit de l'indépendance américaine perdure à travers chaque brique et monument.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Sigue los pasos de la historia a lo largo de los caminos empedrados de Beacon Hill. Desde la grandeur del Quincy Market hasta los muelles históricos del puerto, encuentra una ciudad donde el espíritu de la independencia estadounidense perdura a través de cada ladrillo y monumento."
    },
    "new_york": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Experience the restless pulse of the world’s most iconic metropolis. From the shimmering neon of Times Square and the industrial majesty of the Brooklyn Bridge to the quiet, sun-drenched paths of Central Park, witness a city of infinite scales and electric ambitions.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Vivez le pouls incessant de la métropole la plus emblématique du monde. Des néons scintillants de Times Square et de la majesté industrielle du pont de Brooklyn aux sentiers calmes et ensoleillés de Central Park, témoignez d'une ville aux échelles infinies et aux ambitions électriques.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Experimenta el pulso inquieto de la metrópolis más icónica del mundo. Desde el neón brillante de Times Square y la majestuosidad industrial del Puente de Brooklyn hasta los caminos tranquilos y bañados por el sol de Central Park, presencia una ciudad de escalas infinitas y ambiciones eléctricas."
    },
    "montreal": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Feel the dual soul of North America’s most eclectic island. From the adrenaline of the Formula 1 tracks and towering street murals to the glowing neon of the Quartier des Spectacles, capture the vibrant pulse of a city that lives for the moment.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Ressentez la double âme de l'île la plus éclectique d'Amérique du Nord. De l'adrénaline des pistes de Formule 1 et des fresques murales imposantes aux néons brillants du Quartier des Spectacles, capturez le pouls vibrant d'une ville qui vit pour le moment.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Siente el alma dual de la isla más ecléctica de América del Norte. Desde la adrenalina de las pistas de Fórmula 1 y los imponentes murales callejeros hasta el neón brillante del Quartier des Spectacles, captura el pulso vibrante de una ciudad que vive el momento."
    },
    "montenegro": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Behold the dramatic meeting of jagged limestone peaks and crystalline waters. Navigate through the winding Bay of Kotor, where ancient stone villages cling to the shoreline beneath the watchful gaze of mountain fortresses—a true hidden gem of the Adriatic.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplez la rencontre dramatique de pics calcaires déchiquetés et d'eaux cristallines. Naviguez dans la baie sinueuse de Kotor, où d'anciens villages de pierre s'accrochent au rivage sous le regard attentif des forteresses de montagne—un véritable joyau caché de l'Adriatique.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Contempla el encuentro dramático de picos de piedra caliza irregulares y aguas cristalinas. Navega por la sinuosa Bahía de Kotor, donde antiguos pueblos de piedra se aferran a la costa bajo la atenta mirada de fortalezas de montaña, una verdadera joya oculta del Adriático."
    },
    "maine": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Surrender to the rugged charm of the Pine Tree State. From the historic beacons of Portland Head Light to the bustling docks of fishing harbors, discover a coastline where the deep blue Atlantic carves its story into granite shores and salty traditions.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Abandonnez-vous au charme sauvage de l'État du Pin. Des phares historiques de Portland Head Light aux quais animés des ports de pêche, découvrez un littoral où l'Atlantique bleu profond grave son histoire dans les rives de granit et les traditions salées.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Ríndete al encanto robusto del Estado del Pino. Desde los faros históricos de Portland Head Light hasta los bulliciosos muelles de los puertos pesqueros, descubre una costa donde el azul profundo del Atlántico talla su historia en orillas de granito y tradiciones saladas."
    },
    "canada": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Venture into the raw, untamed heart of the Great White North. From close encounters with majestic wildlife in the frozen wilderness to emerald-green shorelines hidden deep within the forest, discover the spontaneous beauty of a land that knows no bounds.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Aventurez-vous dans le cœur brut et indompté du Grand Nord Blanc. Des rencontres rapprochées avec une faune majestueuse dans la nature sauvage gelée aux rivages vert émeraude cachés au fond de la forêt, découvrez la beauté spontanée d'une terre qui ne connaît aucune limite.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Aventúrate en el corazón crudo e indómito del Gran Norte Blanco. Desde encuentros cercanos con la majestuosa vida silvestre en la naturaleza helada hasta las orillas verde esmeralda ocultas en lo profundo del bosque, descubre la belleza espontánea de una tierra que no conoce límites."
    },
    "corse": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Behold the breathtaking cliffs of the 'Isle of Beauty.' From the dizzying heights of Bonifacio perched above the turquoise Mediterranean to the secret emerald pools of inland rivers, discover a land of granite and grit that remains wonderfully untamed.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplez les falaises à couper le souffle de l'île de Beauté. Des hauteurs vertigineuses de Bonifacio perchées au-dessus de la Méditerranée turquoise aux piscines émeraude secrètes des rivières intérieures, découvrez une terre de granit et de cran qui reste merveilleusement indomptée.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Contempla los impresionantes acantilados de la 'Isla de la Belleza'. Desde las alturas vertiginosas de Bonifacio encaramadas sobre el Mediterráneo turquesa hasta las piscinas esmeralda secretas de los ríos interiores, descubre una tierra de granito y valor que permanece maravillosamente indómita."
    },
    "niagara_falls": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Stand at the edge of the world where thunderous waters meet a neon-lit skyline. Witness the overwhelming force of the falls in all their misty glory, before wandering into the vibrant, cinematic energy of Niagara City’s bustling streets and retro motels.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Tenez-vous au bord du monde où les eaux tonitruantes rencontrent un horizon éclairé au néon. Témoignez de la force écrasante des chutes dans toute leur gloire brumeuse, avant de vous promener dans l'énergie vibrante et cinématographique des rues animées et des motels rétro de Niagara City.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Párate en el borde del mundo donde las aguas atronadoras se encuentran con un horizonte iluminado por neón. Presencia la fuerza abrumadora de las cataratas en toda su gloria brumosa, antes de vagar por la energía vibrante y cinematográfica de las bulliciosas calles y moteles retro de la ciudad de Niágara."
    },
    "ottawa": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Witness a capital in full bloom. From the vibrant endless fields of the Canadian Tulip Festival to the scenic pathways along the Rideau Canal, explore a city where nature's bright palette perfectly complements the historic stone of Parliament Hill.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Témoignez d'une capitale en pleine floraison. Des champs infinis et vibrants du Festival canadien des tulipes aux sentiers pittoresques le long du canal Rideau, explorez une ville où la palette lumineuse de la nature complète parfaitement la pierre historique de la Colline du Parlement.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Presencia una capital en plena floración. Desde los vibrantes campos interminables del Festival Canadiense de los Tulipanes hasta los pintorescos senderos a lo largo del Canal Rideau, explora una ciudad donde la paleta brillante de la naturaleza complementa perfectamente la pierre historique de la Colline du Parlement."
    },
    "quebec": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Step into a living fairy tale where cobblestone streets meet the majestic silhouette of the Château Frontenac. From the frost-covered ramparts to the warm glow of Petit Champlain at night, witness the romantic soul of North America’s oldest fortified city.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Entrez dans un conte de fées vivant où les rues pavées rencontrent la silhouette majestueuse du Château Frontenac. Des remparts couverts de givre à la lueur chaude du Petit Champlain la nuit, témoignez de l'âme romantique de la plus vieille ville fortifiée d'Amérique du Nord.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Entra en un cuento de hadas viviente donde las calles empedradas se encuentran con la majestuosa silueta del Château Frontenac. Desde las murallas cubiertas de escarcha hasta el cálido resplandor de Petit Champlain por la noche, presencia el alma romántica de la ciudad fortificada más antigua de América del Norte."
    },
    "philadelphie": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Immerse yourself in a vibrant urban mosaic where history meets bold creativity. From the intricate glass masterpieces of the Magic Gardens to the towering blue spans of the Ben Franklin Bridge, discover the colorful soul and resilient spirit of the City of Brotherly Love.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Plongez-vous dans une mosaïque urbaine vibrante où l'histoire rencontre une créativité audacieuse. Des chefs-d'œuvre de verre complexes des Magic Gardens aux travées bleues imposantes du pont Ben Franklin, découvrez l'âme colorée et l'esprit résilient de la ville de l'amour fraternel.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Sumérgete en un vibrante mosaico urbano donde la historia se encuentra con la creatividad audaz. Desde las intrincadas obras maestras de vidrio de los Jardines Mágico de Filadelfia hasta los imponentes tramos azules del Puente Ben Franklin, descubre el alma colorida y el espíritu resistente de la Ciudad del Amor Fraternal."
    },
    "miami": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Dive into the electric energy of the Vice City. From the pastel-hued Art Deco facades of Ocean Drive to the sun-soaked shores of South Beach, experience a world where tropical glamour meets a vibrant, multicultural pulse.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Plongez dans l'énergie électrique de la \"Vice City\". Des façades Art déco aux teintes pastel d'Ocean Drive aux rives ensoleillées de South Beach, découvrez un monde où le glamour tropical rencontre un pouls multiculturel vibrant.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Sumérgete en la energía eléctrica de la \"Vice City\". Desde las fachadas Art Deco en tonos pastel de Ocean Drive hasta las costas bañadas por el sol de South Beach, descubre un mundo donde el glamour tropical se encuentra con un vibrante pulso multicultural."
    },
    "keys": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Follow the Overseas Highway to a realm of turquoise waters and island time. From the historic charm of Key West’s colorful streets to the serene beauty of coral reefs, discover a Caribbean-style paradise at the southernmost tip of the United States.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Suivez l'Overseas Highway vers un royaume d'eaux turquoise et de temps suspendu. Du charme historique des rues colorées de Key West à la beauté sereine des récifs coralliens, découvrez un paradis de style caraïbe à la pointe sud des États-Unis.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Sigue la Overseas Highway hacia un reino de aguas turquesas y tiempo pausado. Desde el encanto histórico de las coloridas calles de Key West hasta la belleza serena de los arrecifes de coral, descubre un paraíso de estilo caribeño en el extremo sur de los Estados Unidos."
    },
    "everglades": {
        "en": "&nbsp;&nbsp;&nbsp;&nbsp;Venture into the mysterious 'River of Grass'. From the ancient sawsedge marshes to the hidden alligator trails beneath the cypress canopy, witness a unique wilderness where water and sky merge in a silent, primordial dance.",
        "fr": "&nbsp;&nbsp;&nbsp;&nbsp;Aventurez-vous dans la mystérieuse \"Rivière d'Herbe\". Des anciens marais de scirpe aux sentiers cachés des alligators sous la canopée des cyprès, témoignez d'une nature sauvage unique où l'eau et le ciel se fondent dans une danse silencieuse et primordiale.",
        "es": "&nbsp;&nbsp;&nbsp;&nbsp;Aventúrate en el misterioso \"Río de Hierba\". Desde las antiguas marismas de juncos hasta los senderos ocultos de los caimanes bajo el dosel de los cipreses, presencia una naturaleza salvaje única donde el agua y el cielo se funden en una danza silenciosa y primordial."
    }
}

def clean_name(name):
    name = name.lower().replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]+', '', name)
    return name.strip('_')

def get_exif_data(img_path):
    """Extrait les réglages techniques de l'image"""
    try:
        img = Image.open(img_path)
        exif_dict = piexif.load(img.info['exif'])
        model = exif_dict['0th'].get(piexif.ImageIFD.Model, b"").decode().strip()
        f_stop = exif_dict['Exif'].get(piexif.ExifIFD.FNumber)
        iso = exif_dict['Exif'].get(piexif.ExifIFD.ISOSpeedRatings)
        shutter = exif_dict['Exif'].get(piexif.ExifIFD.ExposureTime)
        parts = []
        if model: parts.append(model)
        if f_stop: parts.append(f"f/{f_stop[0]/f_stop[1]}")
        if shutter:
            val = f"{shutter[0]}/{shutter[1]}s" if shutter[1] > 1 else f"{shutter[0]}s"
            parts.append(val)
        if iso: parts.append(f"ISO {iso}")
        return " | ".join(parts)
    except Exception:
        return ""

def sync_portfolio():
    if os.path.exists(CONTENT_DIR): shutil.rmtree(CONTENT_DIR)
    if os.path.exists(ASSETS_DIR): shutil.rmtree(ASSETS_DIR)
    
    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for folder in os.listdir(SOURCE_DIR):
        source_folder_path = os.path.join(SOURCE_DIR, folder)
        if not os.path.isdir(source_folder_path): continue
        
        folder_clean = clean_name(folder)
        display_title = folder.replace('_', ' ').title()
        
        hugo_content_path = os.path.join(CONTENT_DIR, folder_clean)
        hugo_assets_path = os.path.join(ASSETS_DIR, folder_clean)
        os.makedirs(hugo_content_path, exist_ok=True)
        os.makedirs(hugo_assets_path, exist_ok=True)

        # On prépare le bloc HTML qui ira dans {{< gallery >}}
        inner_gallery_html = ""

        # --- 1. AJOUT DES VIDÉOS SI ELLES EXISTENT ---
        if folder_clean in VIDEOS:
            for v_url in VIDEOS[folder_clean]:
                inner_gallery_html += f'  <video autoplay loop muted playsinline preload="metadata" class="video-element"><source src="{v_url}" type="video/mp4"></video>\n'

        # --- 2. TRAITEMENT ET AJOUT DES IMAGES ---
        images = [f for f in os.listdir(source_folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]
        for i, img_name in enumerate(sorted(images)):
            img_num = i + 1
            img_clean = f"{folder_clean}_{img_num:03d}.webp"
            full_source_path = os.path.join(source_folder_path, img_name)
            target_path = os.path.join(hugo_assets_path, img_clean)
            
            exif_info = get_exif_data(full_source_path)
            alt_text = f"Photographie de {display_title} - {img_num}"
            
            try:
                img = Image.open(full_source_path)
                img = ImageOps.exif_transpose(img)
                width, height = img.size
                
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    width, height = MAX_WIDTH, new_height 

                inner_gallery_html += f'  <img src="/gallery/{folder_clean}/{img_clean}" alt="{alt_text}" title="{exif_info}" width="{width}" height="{height}" loading="lazy" decoding="async" />\n'
                img.save(target_path, "WEBP", quality=QUALITY, method=6)
                
            except Exception as e:
                print(f"❌ Erreur sur {img_name}: {e}")

        if images:
            first_img_renamed = f"{folder_clean}_001.webp"
            shutil.copy(os.path.join(hugo_assets_path, first_img_renamed), 
                        os.path.join(hugo_content_path, "feature.webp"))

        # Langues à générer
        languages = {
            "en": {"file": "index.md", "title_prefix": "Discover my photo gallery of", "desc_prefix": "A collection of shots capturing the architecture and atmosphere of"},
            "fr": {"file": "index.fr.md", "title_prefix": "Découvrez ma galerie photo de", "desc_prefix": "Une collection de clichés capturant l'architecture et l'ambiance de"},
            "es": {"file": "index.es.md", "title_prefix": "Descubre mi galería de fotos de", "desc_prefix": "Una colección de tomas capturando la arquitectura y la atmósfera de"}
        }

        gallery_desc_map = DESCRIPTIONS.get(folder_clean, {})
        if isinstance(gallery_desc_map, str):
            gallery_desc_map = {"en": gallery_desc_map, "fr": gallery_desc_map, "es": gallery_desc_map}

        for lang, config in languages.items():
            filename = config["file"]
            meta_desc = f"{config['title_prefix']} {display_title}. {config['desc_prefix']} {display_title}."
            gallery_desc = gallery_desc_map.get(lang, "")

            with open(os.path.join(hugo_content_path, filename), "w") as f:
                f.write(f'---\ntitle: "{display_title}"\ndescription: "{meta_desc}"\nlayout: "gallery"\n---\n\n')
                if gallery_desc:
                    f.write(f'<div class="gallery-description max-w-2xl mx-auto mb-8 text-neutral-600 dark:text-neutral-400 tracking-wide">\n{gallery_desc}\n</div>\n\n')
                
                f.write(f'{{{{< gallery >}}}}\n{inner_gallery_html}{{{{< /gallery >}}}}')
        
        print(f"✅ Dossier traité : {folder} -> {folder_clean} (EN, FR, ES)")

if __name__ == "__main__":
    sync_portfolio()