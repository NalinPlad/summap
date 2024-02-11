<script>
  import Counter from './Counter.svelte';
  import welcome from '$lib/images/svelte-welcome.webp';
  import welcome_fallback from '$lib/images/svelte-welcome.png';

  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  import data from '$lib/data.json';
  import icon from '$lib/images/icon.png'


  let el;

  let selected = 0;

  let allLines;

  onMount(() => {
  	var mymap = L
  		.map("map")
		.on('click', _ => {
			// selected = 0;
			// draw();
		})
  		.setView([50, -0.1], 4);

  	// Add a tile to the map = a background. Comes from OpenStreetmap
  	L.tileLayer(
  		'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
  		// maxZoom: 6,
  		}).addTo(mymap);


  	let hcIcon = L.icon({
  		iconUrl: icon,
  		// shadowUrl: 'leaf-shadow.png',

  		iconSize:     [20, 20], // size of the icon
  		// shadowSize:   [50, 64], // size of the shadow
  		iconAnchor:   [10, 10], // point of the icon which will correspond to marker's location
  		// shadowAnchor: [4, 62],  // the same for the shadow
  		popupAnchor:  [0, -10] // point from which the popup should open relative to the iconAnchor
  	});


  	// console.log(data.length);

  	let colors = ["red", "yellow", "blue", "green", "orange", "pink"]

	  
  	function draw() {
		let pLineGroup = L.layerGroup()
		console.log(selected);
  		data.forEach(group => {
			console.log(group);
  			let groupPoints = []
  			group.members.forEach(member => {
  				// console.log(member);
  				let split = member.location.split(',');
  				let lat = parseFloat(split[0]);
  				let long = parseFloat(split[1].slice(1));

  				if(selected == 0 || selected == group.id) {
  					console.log(`Drawing because ${group.id} == ${selected}	`);
  					groupPoints.push([lat,long])
  				}

  				let marker = L.marker([lat, long], {icon: hcIcon }).addTo(mymap)
  				.bindPopup(`<div style="display:flex; flex-direction: column;"><b style="font-size:15pt;margin-bottom: 5px;">${member.name}</b><b style="margin-bottom: 10px;">Project: ${group.project}</b><img src="${member.portrait}" style="width: 200px; border-radius: 5px;"/></div>`)
  				.on('click', _ => {
  					selected = group.id;
  					pLineGroup.remove();
					// console.log(selected);
  					draw();
  				});
  			});

  			pLineGroup.addLayer(L.polyline(groupPoints, {
  				// color: colors[Math.floor(Math.random() * colors.length)],
  				color: 'red',
  				weight: 3,
  				opacity: 0.8,
  				smoothFactor: 1
  			})).addTo(mymap);
		});
  	}

  	draw();
  });
</script>

<svelte:head>
  <title>Home</title>
  <meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
  <!-- <h1>Leaders!</h1> -->

  <div bind:this="{el}" id="map" class="chart"></div>

  <!-- <img src="https://cloud-8xmvp7jvs-hack-club-bot.vercel.app/0_bmt4412.jpg" alt="leaders"/> -->
</section>

<style>
  .chart {
    background-color: #f4f4f4;
    width: 100vw;
    height: 100vh;
    max-width: 100%;
    max-height: 100%;
  }
</style>
