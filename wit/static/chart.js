graph_path = document.getElementById('graph').getAttribute('data-graph-path')
d3.json(graph_path).then(function chart(data) {
  const scale = 500;
  const stroke_width = 20;

  function size(d) {
    const sizes = {
      "entity": 0.2 * scale,
      "statement": 0.3 * scale
    }
    return sizes[d.type];
  }

  function radial(d) {
    const radii = {
      "entity": 5 * scale,
      "statement": 0
    }
    return radii[d.type];
  }

  function fill(d) {
    const colors = {
      "entity": "#b48ead",
      "statement": "#a3be8c"
    }
    return colors[d.type]; 
  }

  function stroke(d) {
    const colors = {
      "READ": "#a3be8c",
      "WRITE": "#ebcb8b",
      "ADMIN": "#bf616a",
      "MEMBER": "#434c5e",
      "MAINTAINER": "#2e3440"
    }
    return "#434c5e";
  }

  const width = 1500;
  const height = 1500;

  const links = data.links.map(d => Object.create(d));
  const nodes = data.nodes.map(d => Object.create(d));

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(2*scale))
      .force("collide", d3.forceCollide(d => size(d)))
      .force("charge", d3.forceManyBody(-130))
      .force("center", d3.forceCenter(width / 2, height / 2))
      //.force("radial", d3.forceRadial(d => radial(d), width/2, height/2))
      //.stop();

  const svg_top = d3.select("svg#graph")
      .attr("viewBox", [0, 0, width, height])
      .on("click", svgClick);

  const svg = svg_top.append("g");

  svg_top.call(d3.zoom().on("zoom", function () {
         svg.attr("transform", d3.event.transform);
      }));

  //for (var i=0; i < 100; i++) simulation.tick();

  d3.select("text#loading").remove();

  const link = svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("source-id", d => d.source.id)
      .attr("target-id", d => d.target.id)
      .attr("stroke-width", stroke_width)
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

  /*
  // Avatars
  const defs = svg.append('defs')
      .selectAll("pattern")
      .data(members)
      .enter()
      .append("pattern")
      .attr("id", d => d.id)
      .attr("width", d => size(d))
      .attr("height", d => size(d))
      .attr("patternUnits", "userSpaceOnUse")
      .append("image")
      .attr("xlink:href", d => d.avatar)
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("preserveAspectRatio", "xMinYMin")
      .attr("x", 0)
      .attr("y", 0);
      */

  const nodelinks = svg.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 0.5 * stroke_width)
      .selectAll("circle")
      .data(nodes)
      .join("a")
      .attr("href", d => d.href);

  const node = nodelinks.append("circle")
      .attr("id", d => d.id)
      .attr("r", d => size(d))
      .attr("fill", d => fill(d))
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .on("mouseover", nodeMouseOver)
      .on("mouseout", nodeMouseOut)
      .on("click", nodeClick);

  node.append("title")
      .text(d => `${d.type}: ${d.label}`);

  simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
  });

  function highlight(d, node, toggle_attr) {
    if (node.attr("select") !== "clicked") {
      d3.selectAll(`line[source-id="${d.id}"], line[target-id="${d.id}"]`).each(function(d, i) {
        const link = d3.select(this);
        link.attr("select", toggle_attr)
            .attr("stroke-width", 2 * stroke_width)
            .attr("stroke-opacity", 1)
            .attr("stroke", d => stroke(d));
        d3.selectAll(`circle#${link.attr("source-id")}`)
          .attr("select", toggle_attr)
          .attr("stroke", "#808080");
        d3.selectAll(`circle#${link.attr("target-id")}`)
          .attr("select", toggle_attr)
          .attr("stroke", "#808080");
      });
      node.attr("select", toggle_attr)
          .attr("stroke", "#101010");
    }
  }

  function unhighlightAll(toggle_attr) {
    d3.selectAll(`line[select="${toggle_attr}"]`)
      .attr("stroke-width", 1 * stroke_width)
      .attr("stroke-opacity", 0.6)
      .attr("stroke", "#999");
    d3.selectAll(`circle[select="${toggle_attr}"]`)
      .attr("select", null)
      .attr("stroke", "#fff");
  }

  function unhighlight(node, toggle_attr) {
    if (node.attr("select") === toggle_attr) {
      unhighlightAll(toggle_attr);
      node.attr("select", null)
          .attr("stroke", "#fff");
    }
  }

  function nodeMouseOver(d, i) {
    highlight(d, d3.select(this), "hover");
    populateInfobox(d);
  }

  function nodeMouseOut(d, i) {
    unhighlight(d3.select(this), "hover");
    hideInfobox();
  }

  function nodeClick(d, i) {
    const node = d3.select(this);
    unhighlightAll("clicked");
    highlight(d, node, "clicked");
    d3.event.stopPropagation();
  }

  function svgClick(d, i) {
    unhighlightAll("clicked");
  }

  function resultMouseOver(d, i) {
    d3.select(`circle#${d.id}`).attr("fill", "#bf616a");
    populateInfobox(d);
  }

  function resultMouseOut(d, i) {
    d3.select(`circle#${d.id}`).attr("fill", fill(d));
    hideInfobox();
  }

  function populateInfobox(d) {
    d3.select("#infobox").attr("data-type", d.type).attr("class", "");
    d3.select("#info-type").text(d.type);
    d3.select("#info-label").text(d.label);
    d3.select("#info-name").text(d.name);
    d3.select("#info-image").attr("src", d.avatar);
  }
  
  function hideInfobox() {
    d3.select("#infobox").attr("class", "hidden");
  }

  // Search
  //const search = document.getElementById("search");
  //search.addEventListener("change", searchChange);

  function searchChange(e) {
    const text = e.srcElement.value.trim();
    const results = d3.select("#search-results");
    results.selectAll("li").remove();
    d3.selectAll("circle").attr("fill", d => fill(d));

    if (text !== "") {
      const items = d3.selectAll("circle").filter(d => `${d.id} ${d.name}`.includes(text));
      if (items.size() > 0) {
        d3.selectAll("circle").attr("fill", "#d8dee9");
        items.attr("fill", d => fill(d));
        results.selectAll("li")
               .data(items.data())
               .enter()
               .append("li")
               .attr("data-type", d => d.type)
               .attr("data-id", d => d.id)
               .text(d => d.label)
               .on("mouseover", resultMouseOver)
               .on("mouseout", resultMouseOut);
      }
    }
  }

  return svg.node();
})
