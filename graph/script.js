async function loadGraphData(num) {
    example = num ? num : 0
    file = "graphs/graph" + example + ".json"
    try {
        const response = await fetch(file);
        const graphData = await response.json();
        drawGraph(graphData);
        drawTree(graphData);
        document.getElementById("json-editor").innerHTML = JSON.stringify(graphData, null, 4);
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", error);
    }
}

function updateGraphData(){
    newGraphData = JSON.parse(document.getElementById("json-editor").value);
    drawGraph(newGraphData);
    drawTree(newGraphData);
    console.log(newGraphData)
}

function drawGraph(graphData) {
    const container = document.getElementById("graph-container");

    const minEdgeLength = 50, maxEdgeLength = 300;
    const maxValue = Math.max(...graphData.edges.map(edge => edge.value));

    const nodes = new vis.DataSet(graphData.nodes.map(node => ({
        ...node,
        font: { size: 16, color: "black" },
        shape: "dot",
        label: node.heuristic ? node.label + "\nh=" + node.heuristic : node.label,
        color: node.start
            ? { background: "#28a745", border: "#1e7e34" }
            : node.end
            ? { background: "#dc3545", border: "#a71d2a" }
            : { background: "#007bff", border: "#0056b3" }
    })));

    const edges = new vis.DataSet(graphData.edges.map(edge => ({
        ...edge,
        font: { align: "top" },
        width: 2,
        label: edge ? edge.value.toString() : "",
        scaling: { min: 2, max: 2 },
        length: minEdgeLength + ((maxEdgeLength - minEdgeLength) * (edge.value / maxValue))
    })));

    new vis.Network(container, { nodes, edges }, {
        edges: { arrows: { to: false }, width: 2 },
        nodes: { borderWidth: 2 },
        physics: { enabled: false, solver: "barnesHut" }
    });
}

function drawTree(graphData) {
    const container = document.getElementById("tree-container");
    const startNode = graphData.nodes.find(node => node.start);
    const endNode = graphData.nodes.find(node => node.end);
    if (!startNode || !endNode) return console.error("Start oder Endknoten fehlt!");

    const treeNodes = new vis.DataSet();
    const treeEdges = new vis.DataSet();
    const queue = [{ id: startNode.id, parent: null }];
    let idTranslate = new Map()
    let counter = 0
    while (queue.length > 0) {
        const { id, parent } = queue.shift();
        const originalNode = graphData.nodes.find(n => n.id === id);
        const newid = 100 + counter;
        idTranslate.set(newid,id)
        treeNodes.add({
            id: newid,
            label: originalNode.heuristic ? originalNode.label + "\nh=" + originalNode.heuristic : originalNode.label,
            color: originalNode.start
                ? { background: "#28a745", border: "#1e7e34" }
                : originalNode.end
                ? { background: "#dc3545", border: "#a71d2a" }
                : { background: "#007bff", border: "#0056b3" }
        });
        counter++;

        if (parent !== null) {
            const edge = graphData.edges.find(e => e.from === idTranslate.get(parent) && e.to === idTranslate.get(newid));
            treeEdges.add({ from: parent, to: newid, label: edge ? edge.value.toString() : "" });
        }

        const neighbors = graphData.edges.filter(edge => edge.from === id).map(edge => edge.to);
        neighbors.forEach(neighbor => {
            queue.push({ id: neighbor, parent: newid });
        });
    
    }

    new vis.Network(container, { nodes: treeNodes, edges: treeEdges }, {
        edges: { arrows: { to: false }, width: 2, font: { align: "top" } },
        nodes: { shape: "box", borderWidth: 2, font: { size: 16, color: "white" } },
        layout: { hierarchical: { direction: "UD", sortMethod: "directed", levelSeparation: 100, nodeSpacing: 100 } },
        physics: false
    });
}