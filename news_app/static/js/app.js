console.log("app.js is running!")

// function animatedHeatmap() {
// 	d3.json("http://project3-news-app.herokuapp.com/static/js/animation.json").then(function (jsonData) {
// 		console.log(jsonData)
// 	})
// }

function userAnalysis() {
    console.log("Running user analysis in app.py")
    var userText = d3.select("#user-text-input").property("value")
    console.log(`User text: ${userText}`)

    fetch(`${window.origin}/interactive/user-sentiment`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(userText),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
	})
	.then(function (response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function (responseJson) {
            console.log(responseJson)
            
			Plotly.newPlot("user-analysis-gauge", responseJson.gauge_data)
			Plotly.newPlot("user-analysis-emotions", responseJson.emotion_plot_data, responseJson.emotion_plot_layout)

			$.scrollTo($('#user-analysis-intro'), 700);
		})
	})
	.catch(function (error) {
		console.log("Fetch error: " + error)
	})
}


function articleSearch() {
    console.log("Running articleSearch() in app.py")
	var keywordType = d3.select("#keyword-type").property("value")
	var searchInput = d3.select("#article-search-input").property("value")
	console.log(`Keyword Type: ${keywordType}`)
	console.log(`Search Input: ${searchInput}`)

	searchDict = {
		keyword: keywordType,
		find: searchInput,
	}

    fetch(`${window.origin}/interactive/article-search`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(searchDict),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
	})
	.then(function (response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function (responseJson) {
			console.log(responseJson)
			
            
			var clear_results = d3.select("#article-search-output")
                if (clear_results._groups[0][0].hasChildNodes()) {
					clear_results.selectAll("div").remove()
					}
			
			var outputDiv = d3.select("#article-search-output")

			for (i = 0; i < responseJson.articles.length; i++) {
				newRow = outputDiv.append("div")
					.classed("row", true)
					.classed("ouput-div", true)
					.property("id", `row-${i}`)
					.attr("dy", "1em")
				
				articleColumn = newRow.append("div")
					.classed("col-md-6", true)
					.classed("ouput-div", true)
					.property("id", `article-${i}`)

				articleColumn.append("h4")
					.text(responseJson.headlines[i])

				articleLocations = eval(responseJson.locations[i])
				articleDate = responseJson.dates[i]

				articleByline = articleColumn.append("p")
					.classed("lead", true)
					.text(function () {
						let bylineString = ""
						bylineString += articleDate
						console.log(bylineString)
						if (articleLocations.length) {
							articleLocations.forEach(location => {
								bylineString += ` | ${location}`
							})
						}
						return bylineString
					})
					

				articleDiv = articleColumn.append("div")
					.classed("article-scrollable", true)

				articleDiv.append("p")
					.text(`${responseJson.articles[i]}`)

				gaugeColumn = newRow.append("div")
					.classed("col-md-6", true)
					.classed("ouput-div", true)
					.property("id", `gauge-${i}`)

				Plotly.newPlot(`gauge-${i}`, responseJson.gauges[i])

				$.scrollTo($('#article-search-intro'), 700);
			}
			
					// var table = d3.select('#dice-table')
			// 	.append('table')
			// 	.classed("center", true)
			// var thead = table.append('thead')
			// var	tbody = table.append('tbody');

			// // append the header row
			// thead.append('tr')
			// .selectAll('th')
			// .data(Object.keys(tableData))
			// .enter()
			// .append('th')
			// .text(d => d);

			// for (i = 0; i < _.size(tableData["Roll Total"]); i++) {
			// 	var row = tbody.append('tr')
			// 	Object.keys(tableData).forEach(column => {
			// 		row.append('td')
			// 		.text(tableData[column][i])
			// 	}) 				
			// }

			// // create a row for each object in the data
			// var rows = tbody.selectAll('tr')
			// .data(tableData["Roll #"])
			// .enter()
			// .append('tr')
			
			// rows.selectAll('td')
			// .data(tableData)
			// .enter()
			// .append('td')
			// .text(d => d)

			
			
		})
	})
	.catch(function (error) {
		console.log("Fetch error: " + error)
	})
}
