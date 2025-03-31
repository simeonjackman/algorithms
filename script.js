async function loadGraphAndTreeData(filename) {
    try {
        const graphData = await loadJSON(filename);
        drawGraph(graphData);
        drawTreeFromGraph(graphData);
        if(document.getElementById("json-editor")){
            document.getElementById("json-editor").innerHTML = JSON.stringify(graphData, null, 4);
        }
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", filename, error);
    }
}

async function loadGraphData(filename) {
    try {
        const graphData = await loadJSON(filename);
        drawGraph(graphData);
        if(document.getElementById("json-editor")){
            document.getElementById("json-editor").innerHTML = JSON.stringify(graphData, null, 4);
        }
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", filename, error);
    }
}

async function loadTreeData(filename) {
    try {
        const graphData = await loadJSON(filename);
        drawTreeFromGraph(graphData);
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", filename, error);
    }
}

async function loadJSON(filename) {
    try {
        const response = await fetch(filename);
        const graphData = await response.json();
        return graphData;
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", filename, error);
    }
}

function updateGraphData(){
    newGraphData = JSON.parse(document.getElementById("json-editor").value);
    drawGraph(newGraphData);
    drawTreeFromGraph(newGraphData);
}

function drawGraph(graphData, treeDepth = 0) {
    const container = document.getElementById("graph-container");
    container.style.display = "block";

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
        label: edge.value ? edge.value.toString() : "",
        scaling: { min: 2, max: 2 }
    })));

    new vis.Network(container, { nodes, edges }, {
        edges: { arrows: { to: false }, width: 2 },
        nodes: { borderWidth: 2 },
        physics: { enabled: false, solver: "barnesHut" }
    });
}

function drawTreeFromGraph(graphData) {
    const container = document.getElementById("tree-container");
    const startNode = graphData.nodes.find(node => node.start);
    const endNode = graphData.nodes.find(node => node.end);
    if (!startNode || !endNode) return console.error("Start oder Endknoten fehlt!");

    const treeNodes = new vis.DataSet();
    const treeEdges = new vis.DataSet();
    const queue = [{ id: startNode.id, parent: null }];
    let newIDs = new Map() // new IDs because we have repetition of nodes in trees
    let counter = 0
    let visited = new Set();
    while (queue.length > 0) {
        const { id, parent } = queue.shift();
        visited.add(id);
        const originalNode = graphData.nodes.find(n => n.id === id);
        const newid = graphData.nodes.length + counter;
        newIDs.set(newid,id);
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
            const edge = graphData.edges.find(e => e.from === newIDs.get(parent) && e.to === newIDs.get(newid));
            treeEdges.add({ from: parent, to: newid, label: edge && edge.value ? edge.value.toString() : "" });
        }
        if (id == endNode.id || newIDs.get(id) == endNode.id){
            continue;
        }
        const neighborsFrom = graphData.edges.filter(edge => edge.from === id).map(edge => edge.to);
        const neighborsTo = graphData.edges.filter(edge => edge.to === id).map(edge => edge.from);
        const neighbors = neighborsFrom.concat(neighborsTo);
        neighbors.forEach(neighbor => {
            if (neighbor == endNode.id || !visited.has(neighbor)) {
                queue.push({ id: neighbor, parent: newid, heuristic: graphData.nodes.find(n => n.id === neighbor || n.id === newIDs.get(neighbor)).heuristic});
                queue.sort((a, b) => a.heuristic - b.heuristic);
            }
        });
    }

    new vis.Network(container, { nodes: treeNodes, edges: treeEdges }, {
        edges: { arrows: { to: false }, width: 2, font: { align: "top" } },
        nodes: { shape: "box", borderWidth: 2, font: { size: 16, color: "white" } },
        layout: { hierarchical: { direction: "UD", sortMethod: "directed", levelSeparation: 100, nodeSpacing: 100 } },
        physics: false
    });
}
