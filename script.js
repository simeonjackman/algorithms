async function loadGraphData() {
    try {
        const response = await fetch("graph.json");
        const graphData = await response.json();
        drawGraph(graphData);
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", error);
    }
}

function drawGraph(graphData) {
    const container = document.getElementById("graph-container");

    // Update nodes to include heuristic values and highlight start/end nodes
    const nodes = new vis.DataSet(graphData.nodes.map(node => ({
        ...node,
        label: `${node.label}\nh=${node.heuristic}`, // Show heuristic inside the node
        font: { size: 16, color: "white" },
        shape: "circle",
        color: node.start
            ? { background: "#28a745", border: "#1e7e34" } // Green for start node
            : node.end
            ? { background: "#dc3545", border: "#a71d2a" } // Red for end node
            : { background: "#007bff", border: "#0056b3" } // Blue for normal nodes
    })));

    // Update edges to remove arrows and set fixed width
    const edges = new vis.DataSet(graphData.edges.map(edge => ({
        ...edge,
        font: { align: "top" }, // Keep edge labels visible
        width: 2 // Fixed edge thickness
    })));

    // Graph data
    const data = { nodes, edges };

    // Graph options
    const options = {
        edges: {
            arrows: { to: false, from: false }, // Removes arrows
            font: { size: 14, color: "black", align: "middle" },
            width: 2 // Set fixed width
        },
        nodes: {
            font: { size: 16, color: "white" },
            borderWidth: 2
        }
    };

    // Create the network
    new vis.Network(container, data, options);
}
