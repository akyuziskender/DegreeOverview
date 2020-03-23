function init() {
    if (window.goSamples) goSamples();  // init for these samples -- you don't need to call this
    var $ = go.GraphObject.make;  // for conciseness in defining templates
    myDiagram =
      $(go.Diagram, "myDiagramDiv",
        {
          allowCopy: false,
          layout:
            $(go.LayeredDigraphLayout,
              {
                setsPortSpots: false,  // Links already know their fromSpot and toSpot
                columnSpacing: 5,
                isInitial: false,
                isOngoing: false
              }),

          validCycle: go.Diagram.CycleNotDirected,
          "undoManager.isEnabled": true
        });

    var graygrad = $(go.Brush, "Linear",
      { 0: "#fff"});


    // MAIN NODE
    myDiagram.nodeTemplateMap.add("Loading",
    $(go.Node, "Spot",
      { selectionAdorned: false, textEditable: false, locationObjectName: "BODY" },
      new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
      // the main body consists of a Rectangle surrounding the text
      $(go.Panel, "Auto",
        { name: "BODY" },
        $(go.Shape, "RoundedRectangle",
          { fill: "white", strokeWidth: 0, minSize: new go.Size(120, 60)}),
        $(go.TextBlock,
          {stroke: "black", font: "20px myFont", editable: false,
            margin: new go.Margin(3, 3 + 11, 3, 3 + 4), alignment: go.Spot.Center,
          },
          new go.Binding("text", "text"))
      ),


      // output port
      $(go.Panel, "Auto",
        { alignment: go.Spot.Right, portId: "from" },
        $(go.Shape, "Rectangle",
        { width: 8, height: 60, fill: "#23374d", strokeWidth:0, margin: new go.Margin(0, 0,0,0) })
      )
    ));

    // CHILD
    myDiagram.nodeTemplate =  // the default node template
      $(go.Node, "Spot",
        { selectionAdorned: false, textEditable: false, locationObjectName: "BODY" },
        new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
        // the main body consists of a Rectangle surrounding the text
        $(go.Panel, "Auto",
          { name: "BODY" },
          $(go.Shape, "Rectangle",
            { fill: graygrad, strokeWidth: 0, minSize: new go.Size(120, 60)}),
          $(go.TextBlock,
            {stroke: "black", font: "20px myFont", editable: false,
              margin: new go.Margin(3, 3 + 11, 3, 3 + 4), alignment: go.Spot.Center,
            },
            new go.Binding("text", "text"))
        ),

        // input port
        $(go.Panel, "Auto",
        { alignment: go.Spot.Left, portId: "to", toLinkable: false },
        $(go.Shape, "Rectangle",
          { width: 8, height: 60, fill: "#fff", strokeWidth:0, margin: new go.Margin(0, 0,0,0) })
        ),
        // output port
        $(go.Panel, "Auto",
          { alignment: go.Spot.Right, portId: "from" },
          $(go.Shape, "Rectangle",
          { width: 8, height: 60, fill: "#fff", strokeWidth:0, margin: new go.Margin(0, 0,0,0) })
        )
      );

      // END NODE
    myDiagram.nodeTemplateMap.add("End",
      $(go.Node, "Spot",
        { selectionAdorned: false, textEditable: false, locationObjectName: "BODY" },
        new go.Binding("location", "loc", go.Point.falseparse).makeTwoWay(go.Point.stringify),
        // the main body consists of a Rectangle surrounding the text
        $(go.Panel, "Auto",
          { name: "BODY" },
          $(go.Shape, "RoundedRectangle",
            { fill: graygrad, strokeWidth: 0, minSize: new go.Size(120, 60)}),
          $(go.TextBlock,
            {stroke: "white", font: "20px myFont", editable: false,
              margin: new go.Margin(3, 3 + 11, 3, 3 + 4), alignment: go.Spot.Center,
            },
            new go.Binding("text", "text"))
        ),

        // input port
        $(go.Panel, "Auto",
          { alignment: go.Spot.Left, portId: "to", toLinkable: false },
          $(go.Shape, "Rectangle",
            { width: 8, height: 60, fill: "#23374d", strokeWidth:0, margin: new go.Margin(0, 0,0,0) })
        )
      ));



    myDiagram.linkTemplate =
    $(go.Link,
      { fromPortId: "from", toPortId: "to",
        curve: go.Link.Bezier,
        fromShortLength: -2,
        toShortLength: -2,
        selectable: false
      },
      $(go.Shape,
        { strokeWidth: 5 },
        new go.Binding("stroke", "toNode", function(n) {
          if (n.data.brush) return n.data.brush;
          return "white";
        }).ofObject())
    ); // the link shape
      /*
      $(go.Link,
        { fromPortId: "from", toPortId: "to",
          curve: go.Link.Bezier,
          toEndSegmentLength: 50, fromEndSegmentLength: 50
        },
        $(go.Shape, {stroke: "#23374d", strokeWidth: 3 }) // the link shape, with the default black stroke
      );*/

    function commonLinkingToolInit(tool) {
      // the temporary link drawn during a link drawing operation (LinkingTool) is thick and blue
      tool.temporaryLink =
        $(go.Link, { layerName: "Tool" },
          $(go.Shape, { stroke: "dodgerblue", strokeWidth: 0 }));

      // change the standard proposed ports feedback from blue rectangles to transparent circles
      tool.temporaryFromPort.figure = "Circle";
      tool.temporaryFromPort.stroke = null;
      tool.temporaryFromPort.strokeWidth = 0;
      tool.temporaryToPort.figure = "Circle";
      tool.temporaryToPort.stroke = null;
      tool.temporaryToPort.strokeWidth = 0;

      // provide customized visual feedback as ports are targeted or not

    }

    var ltool = myDiagram.toolManager.linkingTool;
    commonLinkingToolInit(ltool);
    // do not allow links to be drawn starting at the "to" port
    ltool.direction = go.LinkingTool.ForwardsOnly;

    var rtool = myDiagram.toolManager.relinkingTool;
    commonLinkingToolInit(rtool);
    // change the standard relink handle to be a shape that takes the shape of the

    // use a special DraggingTool to cause the dragging of a Link to start relinking it
    myDiagram.toolManager.draggingTool = new DragLinkingTool();

    // detect when dropped onto an occupied cell
    myDiagram.addDiagramListener("SelectionMoved", shiftNodesToEmptySpaces);

    function shiftNodesToEmptySpaces() {
      myDiagram.selection.each(function(node) {
        if (!(node instanceof go.Node)) return;
        // look for Parts overlapping the node
        while (true) {
          var exist = myDiagram.findObjectsIn(node.actualBounds,
            // only consider Parts
            function(obj) { return obj.part; },
            // ignore Links and the dropped node itself
            function(part) { return part instanceof go.Node && part !== node; },
            // check for any overlap, not complete containment
            true).first();
          if (exist === null) break;
          // try shifting down beyond the existing node to see if there's empty space
          node.position = new go.Point(node.actualBounds.x, exist.actualBounds.bottom + 10);
        }
      });
    }

    // prevent nodes from being dragged to the left of where the layout placed them
    myDiagram.addDiagramListener("LayoutCompleted", function(e) {
      myDiagram.nodes.each(function(node) {
        if (node.category === "Recycle") return;
        node.minLocation = new go.Point(node.location.x, node.location.y);
        node.maxLocation = new go.Point(node.location.x, node.location.y)
      });
    });

    load();  // load initial diagram from the mySavedModel textarea
  }


  function load() {
    myDiagram.model = go.Model.fromJson(document.getElementById("mySavedModel").value);
    // if any nodes don't have a real location, explicitly do a layout
    if (myDiagram.nodes.any(function(n) { return !n.location.isReal(); })) layout();
  }

  function layout() {
    myDiagram.layoutDiagram(true);
  }


  // Define a custom tool that changes a drag operation on a Link to a relinking operation,
  // but that operates like a normal DraggingTool otherwise.
  function DragLinkingTool() {
    go.DraggingTool.call(this);
    this.isGridSnapEnabled = true;
    this.isGridSnapRealtime = false;
    this.gridSnapCellSize = new go.Size(500, 1);
    this.gridSnapOrigin = new go.Point(10.5, 10);
  }

  //go.Diagram.inherit(DragLinkingTool, go.DraggingTool);

  // Handle dragging a link specially -- by starting the RelinkingTool on that Link/*
  /*DragLinkingTool.prototype.doActivate = function() {
    var diagram = this.diagram;
    if (diagram === null) return;
    this.standardMouseSelect();
    var main = this.currentPart;  // this is set by the standardMouseSelect

    if (main instanceof go.Link) { // maybe start relinking instead of dragging
      var relinkingtool = diagram.toolManager.relinkingTool;
      // tell the RelinkingTool to work on this Link, not what is under the mouse
      relinkingtool.originalLink = main;
      // start the RelinkingTool
      diagram.currentTool = relinkingtool;
      // can activate it right now, because it already has the originalLink to reconnect
      relinkingtool.doActivate();
      relinkingtool.doMouseMove();
    } else {
      go.DraggingTool.prototype.doActivate.call(this);
    }
  };*/
  // end DragLinkingTool
