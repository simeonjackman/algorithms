var maxDepth;
var lastGraphData;
var pruning = true;

setPruningText();

async function loadGraphAndTreeData(filename,maxTreeDepth=5) {
    maxDepth = maxTreeDepth;
    if(document.getElementById("max-depth")){
        document.getElementById("max-depth").innerHTML = maxTreeDepth;
    }
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

async function loadTreeData(filename,maxTreeDepth=5) {
    maxDepth = maxTreeDepth;
    if(document.getElementById("max-depth")){
        document.getElementById("max-depth").innerHTML = maxTreeDepth;
    }
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
        lastGraphData = graphData;
        return graphData;
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", filename, error);
    }
}

function updateGraphData(){
    newGraphData = JSON.parse(document.getElementById("json-editor").value);
    lastGraphData = newGraphData;
    drawGraph(newGraphData);
    drawTreeFromGraph(newGraphData);
}

function drawGraph(graphData = lastGraphData) {
    const container = document.getElementById("graph-container");
    container.style.display = "block";

    const nodes = new vis.DataSet(graphData.nodes.map(node => ({
        ...node,
        font: { size: 16, color: "black" },
        shape: "dot",
        label: node.heuristic ? node.label + "\nh=" + node.heuristic : node.label,
        color: getNodeColor(node)
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
        physics: { enabled: true, solver: "barnesHut" }
    });
}

function hideGraph() {
    const container = document.getElementById("graph-container");
    container.style.display = "none";
}

function hideTree() {
    const container = document.getElementById("tree-container");
    container.style.display = "none";
}

function drawTreeFromGraph(graphData = lastGraphData) {
    const container = document.getElementById("tree-container");
    container.style.display = "block";
    const startNode = graphData.nodes.find(node => node.start);
    const endNodes = graphData.nodes.filter(node => node.end);
    if (!startNode || !endNodes) return console.error("Start oder Endknoten fehlt!");

    const treeNodes = new vis.DataSet();
    const treeEdges = new vis.DataSet();
    const queue = [{ id: startNode.id, parent: null, depth: 0 }];
    let newIDs = new Map() // new IDs because we have repetition of nodes in trees
    let newIDCounter = 0
    let visited = new Set();
    while (queue.length > 0) {
        const { id, parent, depth } = queue.shift();
        if (depth > maxDepth){
            break;
        }
        if (pruning){
            visited.add(id);
        }
        const originalNode = graphData.nodes.find(n => n.id === id);
        const newid = graphData.nodes.length + newIDCounter;
        newIDs.set(newid,id);
        treeNodes.add({
            id: newid,
            label: originalNode.heuristic ? originalNode.label + "\nh=" + originalNode.heuristic : originalNode.label,
            color: getNodeColor(originalNode)
        });
        newIDCounter++;
        if (parent !== null) {
            const edge = graphData.edges.find(e => (e.from === newIDs.get(parent) && e.to === newIDs.get(newid)) || e.from === newIDs.get(newid) && e.to === newIDs.get(parent));
            treeEdges.add({ from: parent, to: newid, label: edge && edge.value ? edge.value.toString() : "" });
        }
        if (endNodes.map(node => node.id).includes(id) || endNodes.map(node => node.id).includes(newIDs.get(id))){
            continue;
        }
        const neighborsFrom = graphData.edges.filter(edge => edge.from === id).map(edge => edge.to);
        const neighborsTo = graphData.edges.filter(edge => edge.to === id).map(edge => edge.from);
        const neighbors = neighborsFrom.concat(neighborsTo);
        neighbors.forEach(neighbor => {
            if (endNodes.map(node => node.id).includes(neighbor) || !visited.has(neighbor)) {
                queue.push({ id: neighbor, parent: newid, heuristic: graphData.nodes.find(n => n.id === neighbor || n.id === newIDs.get(neighbor)).heuristic, depth: depth + 1});
                //queue.sort((a, b) => a.heuristic - b.heuristic);
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

function getNodeColor(node){
    if (node.start){
        return { background: "#28a745", border: "#1e7e34" }
    }
    if (node.end) {
        return { background: "#dc3545", border: "#a71d2a" }
    }
    return { background: "#007bff", border: "#0056b3" }
}

function increaseMaxDepth(){
    maxDepth = Math.min(++ maxDepth, 11);
    document.getElementById("max-depth").innerHTML = maxDepth;
    drawTreeFromGraph();
}

function decreaseMaxDepth(){
    maxDepth = Math.max(-- maxDepth, 0);
    document.getElementById("max-depth").innerHTML = maxDepth;
    drawTreeFromGraph();
}

function togglePruning(){
    pruning = !pruning;
    setPruningText()
    drawTreeFromGraph();
}

function setPruningText(){
    if(document.getElementById("toggle-pruning")){
        document.getElementById("toggle-pruning").innerHTML = pruning ? "Pruning ausschalten" : "Pruning einschalten";
    }
}