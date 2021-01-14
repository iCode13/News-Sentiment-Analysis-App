console.log("hello")

d3.json("static/resources/calendar_heatmap.json").then((plot_data) => {
    console.log("hello")
    console.log(plot_data)
    Plotly.newPlot("calendar-heatmap", plot_data)
})
