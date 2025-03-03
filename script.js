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

    // Scaling factor for edge lengths (adjust this to fine-tune distances)
    const lengthScalingFactor = 10; 

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

    // Update edges: Remove arrows, set fixed width, and adjust length based on cost
    const edges = new vis.DataSet(graphData.edges.map(edge => ({
        ...edge,
        font: { align: "top" }, // Keep edge labels visible
        width: 2, // Fixed edge thickness
        length: edge.value * lengthScalingFactor // Dynamic length adjustment
    })));

    // Graph data
    const data = { nodes, edges };

    // Graph options
    const options = {
        physics: {
            barnesHut: {
                gravitationalConstant: -3000, // Adjusts spacing between clusters
                springLength: 100, // Default length, overridden by `length` in edges
                springConstant: 0.04 // Controls stiffness of connections
            }
        },
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
