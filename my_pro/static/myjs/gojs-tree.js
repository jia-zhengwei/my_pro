
    var GO= go.GraphObject.make;  // for conciseness in defining templates
    var my_node;

    myDiagram =
      GO(go.Diagram, "myDiagramDiv",
        {
          initialAutoScale: go.Diagram.UniformToFill,
          allowDrop: true,
          maxSelectionCount: 1,
          // define the layout for the diagram
          layout: GO(go.TreeLayout, { nodeSpacing: 5, layerSpacing: 30 }),
          "ChangedSelection": onSelectionChanged,
          "clickCreatingTool.archetypeNodeData": { text: "new node" },
        });

    // Define a simple node template consisting of text followed by an expand/collapse button
    myDiagram.nodeTemplate =
      GO(go.Node, "Horizontal",
        GO(go.Panel, "Auto",
          GO(go.Shape, { fill: "#1F4963", stroke: null }),
          GO(go.TextBlock,
            { font: "bold 13px Helvetica, bold Arial, sans-serif",
              stroke: "white", margin: 3, editable: true},
            new go.Binding("text", "text"))
        ),
        GO("TreeExpanderButton")
      );

    // Define a trivial link template with no arrowhead.
    myDiagram.linkTemplate =
      GO(go.Link,
        { selectable: false },
        GO(go.Shape));  // the link shape

    // create the model for the DOM tree
    myDiagram.model =
      GO(go.TreeModel, {
        isReadOnly: false,  // don't allow the user to delete or copy nodes
        // build up the tree in an Array of node data
        nodeDataArray: nodes
      });

  // 选定一个节点的事件
  function onSelectionChanged(e) {
    var node = e.diagram.selection.first();
    var json_nodes;
    // var my_node;
    $.ajax({
      url:'shownodes/',
      type:'GET',
      async: false,
      data: {'id': node.data.key},
      success:function(result){
          json_nodes = result['nodes_failure'];
          $('#mode_name').html(result['process']);
          $('#pro_id').val(result['process_id']);
      }
    })

    $('#tree_mode').treeview({
        data: json_nodes,
        levels:2,
        expandIcon:"glyphicon glyphicon-plus-sign",
        collapseIcon:'glyphicon glyphicon-minus-sign',
    });
    // console.log($('.list-group').html());
    $('#tree_mode').on('nodeSelected', function(event, data){
      my_node = data;
    })


  }













