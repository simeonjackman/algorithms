async function loadGraphData() {
    try {
        const response = await fetch("graph.json");
        const graphData = await response.json();
        drawGraph(graphData);
        drawTree(graphData);
    } catch (error) {
        console.error("Fehler beim Laden der Graph-Daten:", error);
    }
}

function drawGraph(graphData) {
    const container = document.getElementById("graph-container");

    const minEdgeLength = 50, maxEdgeLength = 300;
    const maxValue = Math.max(...graphData.edges.map(edge => edge.value));

    const nodes = new vis.DataSet(graphData.nodes.map(node => ({
        ...node,
        font: { size: 16, color: "white" },
        shape: "circle",
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
        scaling: { min: 2, max: 2 },
        length: minEdgeLength + ((maxEdgeLength - minEdgeLength) * (edge.value / maxValue))
    })));

    new vis.Network(container, { nodes, edges }, {
        edges: { arrows: { to: false }, width: 2 },
        nodes: { borderWidth: 2 },
        physics: { enabled: true, solver: "barnesHut" }
    });
}

function drawTree(graphData) {
    const container = document.getElementById("tree-container");

    const startNode = graphData.nodes.find(node => node.start);
    const endNode = graphData.nodes.find(node => node.end);
    if (!startNode || !endNode) return console.error("Start oder Endknoten fehlt!");

    const paths = findAllPaths(graphData, startNode.id, endNode.id);

    const treeNodes = new vis.DataSet();
    const treeEdges = new vis.DataSet();
    let nodeIdCounter = 1;
    const nodeMap = new Map();

    paths.forEach(path => {
        let previousNode = null;

        path.forEach((nodeId, index) => {
            const uniqueNodeId = `${nodeId}-${index}`;

            if (!nodeMap.has(uniqueNodeId)) {
                const originalNode = graphData.nodes.find(n => n.id === nodeId);
                const newNode = {
                    font: { size: 16, color: "white" },
                    id: nodeIdCounter,
                    label: originalNode.label,
                    color: originalNode.start
                        ? { background: "#28a745", border: "#1e7e34" }
                        : originalNode.end
                        ? { background: "#dc3545", border: "#a71d2a" }
                        : { background: "#007bff", border: "#0056b3" }
                };

                treeNodes.add(newNode);
                nodeMap.set(uniqueNodeId, nodeIdCounter);
                nodeIdCounter++;
            }

            if (previousNode !== null) {
                treeEdges.add({ from: previousNode, to: nodeMap.get(uniqueNodeId) });
            }

            previousNode = nodeMap.get(uniqueNodeId);
        });
    });

    new vis.Network(container, { nodes: treeNodes, edges: treeEdges }, {
        edges: { arrows: { to: true }, width: 2 },
        nodes: { borderWidth: 2 },
        layout: { hierarchical: { direction: "UD", sortMethod: "directed", levelSeparation: 100, nodeSpacing: 100 } },
        physics: false
    });
}

function findAllPaths(graphData, startId, endId, path = [], paths = []) {
    path.push(startId);

    if (startId === endId) {
        paths.push([...path]);
    } else {
        const neighbors = graphData.edges
            .filter(edge => edge.from === startId)
            .map(edge => edge.to);

        neighbors.forEach(neighbor => {
            if (!path.includes(neighbor)) {
                findAllPaths(graphData, neighbor, endId, path, paths);
            }
        });
    }

    path.pop();
    return paths;
}
