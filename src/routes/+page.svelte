<script>
//   import Counter from './Counter.svelte';
  import welcome from '$lib/images/svelte-welcome.webp';
  import welcome_fallback from '$lib/images/svelte-welcome.png';

  import { onMount } from 'svelte';
//   import * as d3 from 'd3';

  import data from '$lib/data.json';
  import icon from '$lib/images/icon.png'
  import bridge from '$lib/images/bridge.png'


  let el;

  let selected = 0;

  let allLines;

  onMount(() => {
  	var mymap = L
  		.map("map", {
			// zoomSnap: 0,
		})
		.on('click', _ => {
			// selected = 0;
			// draw();
		})
  		.setView([50, -0.1], 4);

  	// Add a tile to the map = a background. Comes from OpenStreetmap
  	L.tileLayer(
  		'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
  	}).addTo(mymap);


	// Add marker at 37.75886297691146, -122.42541183911295
	L.marker([37.75886297691146, -122.42541183911295], {
		icon: L.icon({
			iconUrl: bridge,
			iconSize:     [25, 25], // size of the icon
			iconAnchor:   [15, 15], // point of the icon which will correspond to marker's location
			popupAnchor:  [0, -15] // point from which the popup should open relative to the iconAnchor
		}),
		zIndexOffset: 2000
	}).bindPopup(`<b>SUMMIT 📍 The Lighthouse</b><p>Welcome to Summit Map <i>(Summap)</i>! This is a project by event photographers <a href="https://instagram.com/notmysql">Ajith</a> and <a href="https://instagram.com/jackridesmountainbikes">Jack</a> to show to connections between leaders at <a href="https://summit.hackclub.com/">Summit 2024</a>. Click on a dot to see the leader and view a constellation of their group members!</p><h6>Report any errors to @notmysql on HC Slack. Thanks! Find the <i>hacked</i> source code <a href="https://github.com/NalinPlad/summap">here</a> (all photographs are property of Hack Club, shot by us)</h6>`).addTo(mymap).openPopup();

  
	// function panToAjith() {
	// 	mymap.panTo([37.90861218088131, -122.2952501515231]);
	// }

	// function panToJack() {
	// 	mymap.panTo([37.75886297691146, -122.42541183911295]);
	// }

	// Pan to the marker and zoom into it
	mymap.panTo([37.75886297691146, -100.42541183911295]);
	// mymap.setZoom(12);
	// }).addTo(mymap);

  	let hcIcon = L.icon({
  		iconUrl: icon,
  		// shadowUrl: 'leaf-shadow.png',

  		iconSize:     [20, 20], // size of the icon
  		// shadowSize:   [50, 64], // size of the shadow
  		iconAnchor:   [10, 10], // point of the icon which will correspond to marker's location
  		// shadowAnchor: [4, 62],  // the same for the shadow
  		popupAnchor:  [0, -10] // point from which the popup should open relative to the iconAnchor
  	});
	  let hcIcon_small = L.icon({
  		iconUrl: icon,
  		// shadowUrl: 'leaf-shadow.png',

  		iconSize:     [10, 10], // size of the icon
  		// shadowSize:   [50, 64], // size of the shadow
  		iconAnchor:   [5, 5], // point of the icon which will correspond to marker's location
  		// shadowAnchor: [4, 62],  // the same for the shadow
  		popupAnchor:  [0, -5] // point from which the popup should open relative to the iconAnchor
  	});


  	// console.log(data.length);

  	let colors = ["red", "yellow", "blue", "green", "orange", "pink"]

	let old_selected = "";

	function solve_camera(group) {
		let groupPoints = []
		group.members.forEach(member => {
			let split = member.location.split(',');
			let lat = parseFloat(split[0]);
			let long = parseFloat(split[1].slice(1));
			groupPoints.push([lat,long])
		});
		let bounds = L.latLngBounds(groupPoints);
		mymap.flyToBounds(bounds);
	}
	
	
	function draw() {
		let pLineGroup = L.layerGroup()
		let pIconGroup = L.layerGroup()
		// console.log(selected);
		data.forEach(group => {
			// console.log(group);
			let groupPoints = []
			// if selected group
			if(selected == group.id) {
				// console.log("Solving camera");
				solve_camera(group);
			}
  			group.members.forEach(member => {
  				// console.log(member);
  				let split = member.location.split(',');
  				let lat = parseFloat(split[0]);
  				let long = parseFloat(split[1].slice(1));

				let icon = hcIcon_small;

  				if(selected == 0 || selected == group.id) {
  					// console.log(`Drawing because ${group.id} == ${selected}	`);
  					groupPoints.push([lat,long])
					icon = hcIcon;
  				}

				let marker = L.marker([lat, long], {icon: icon, zIndexOffset: selected == group.id ? 1000 : 0})
				.bindPopup(`<div style="display:flex; flex-direction: column;"><b style="font-size:15pt;margin-bottom: 10px;">${member.name}</b><p style="margin-bottom: 10px; margin-top:0; max-width: 175px;"><b>Project:</b> ${group.project}</p><img src="${member.portrait}" style="width: 175px; border-radius: 5px;"/></div>`)
					.on('click', _ => {
						selected = group.id;
						old_selected = member.name+group.id;
						pLineGroup.remove();
						pIconGroup.remove();
						// console.log(selected);
						draw();
				})
				
				// console.log(member.name, old_selected, member.name == old_selected);
				pIconGroup.addLayer(marker).addTo(mymap);
				if(old_selected == member.name+group.id) {
					// console.log(member.name, old_selected, member.name+group.id == old_selected);
					marker.openPopup();
					mymap.panTo([lat, long]);
					// console.log("Opening popup");
				}

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
  <title>Summap | SUMMIT 2024</title>
  <meta name="description" content="Summit Map = Summap" />
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

  .card {
	/*
	
	*/
  }
</style>
