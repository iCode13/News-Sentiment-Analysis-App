d3.json("news_app/static/resources/calendar_heatmap.json").then((plot_data) => {
    console.log(plot_data)
    Plotly.newPlot("calendar-heatmap", heatmap_data)
})