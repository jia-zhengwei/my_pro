$(document).ready(function() {


    var Node;
    var mode_node;
    var control_node;
    var arr = ['product', 'requirement', 'variation']
    /**
     * 初始化树
     */
    $('#tree').treeview({
        data: ininodes(nodes),
        expandIcon:"glyphicon glyphicon-plus-sign",
        collapseIcon:'glyphicon glyphicon-minus-sign',
        levels: 4,
        onNodeSelected: function(event, data){
            var mode_node;
            Node = data;

            $.ajax({
                url:'shownodes/',
                type:'GET',
                async: false,
                data: {'type': data.tags, 'id': data.id},
                success:function(result){
                    $('#tree_mode').treeview({
                        data: result['nodes_failure'],
                        levels:4,
                        expandIcon:"glyphicon glyphicon-plus-sign",
                        collapseIcon:'glyphicon glyphicon-minus-sign',
                    });
                    return false
                }
            })
        }

    });

    function initree(tree_name, nodes){
        $(tree_name).treeview({
            data: nodes,
            expandIcon:"glyphicon glyphicon-plus-sign",
            collapseIcon:'glyphicon glyphicon-minus-sign',
            levels: 4,
        });
    }





    var _processmenu = [
            {
                type: "divider"
            },
            {
                type: "item",
                icon: "hourglass-1",
                text: "产品特性",
                key: "pro",
                action: function () {
                   layer_open(Node, 'product');
                }
            },
            {
                type: "item",
                icon: "hourglass",
                text: "过程特性",
                key: "proce",
                action: function () {
                    layer_open(Node, 'variation');
                }
            },
            {
                type: "item",
                icon: "gears",
                text: "要求",
                key: "req",
                action: function () {
                    layer_open(Node, 'requirement');
                }
            },

    ]
    var _menuItems = [
            {
                type: "title",
                text: "Modifica"
            },
            {
                type: "item",
                icon: "clone",
                text: "复制",
                key: "copy",
                action: function () {
                    layer.open({
                        type: 2,
                        content: 'http://layim.layui.com',
                        area: ['1000px', '500px'],
                        maxmin: true
                    });
                }
            },
            {
                type: "item",
                icon: "scissors",
                text: "剪切",
                key: "cut",
                action: function () {

                }
            },
            {
                type: "item",
                icon: "clipboard",
                text: "粘贴",
                key: "paste",
                action: function () {

                }
            },
             {
                type: "item",
                icon: "eraser",
                text: "删除",
                key: "delete",
                action: function () {

                }
            },
            {
                type: "item",
                icon: "pencil",
                text: "编辑",
                key: "update",
                action: function () {
                }
            },
    ];


    /**
     *将节点数据修改默认非展开
     */
     function ininodes(nodes){
        var nodes_length = nodes.length;
        for (var i = 0; i < nodes_length; i++) {
            nodes[i]['state']={
                checked: false,
                disabled: false,
                expanded: false,
                selected: false
            };
         }
         return nodes
     }

     /**
     *弹出层的函数实现
     */
     function layer_open(node, str_type){
        var nodeRoot = getRoot(node);
        layer.open({
            type: 2,
            title: nodeRoot.text,
            id:'myiframe',
            shadeClose: true,
            shade: false,
            btn:['提交', '取消'],
            maxmin: true, //开启最大化最小化按钮
            area: ['893px', '600px'],
            content:"addForm/?id="+nodeRoot.id+"&&type="+str_type,
            yes:function (index, layero) {
                var iframeWin = window[layero.find('iframe')[0]['name']];
                var node = iframeWin.submit();
                $('#tree').treeview({
                    data: node['treedata'],
                    showTags: true,
                    onNodeSelected: function (event, data) {
                        iniTree(data);
                        Node = data
                }
                });
                var results = $('#tree').treeview('search', [node['text'],{}]);
                var parent = $('#tree').treeview('getParent', results[0]);
                console.log(parent);
                $('#tree').treeview('toggleNodeSelected', [ parent.nodeId, { silent: true } ]);
                iniTree(parent)
            },
            btn2:function (index, layero) {
                layer.close()
            }
        });
     }

     function layer_mode(node, str_type){
        var parentNode = $('#tree').treeview('getParent', node);
        if(parentNode && parentNode.nodes != null ){
            if ($.inArray(node.tags[0], arr) >= 0)
            layer.open({
                type: 2,
                title: nodeRoot.text,
                id:'myiframe',
                shadeClose: true,
                shade: false,
                btn:['提交', '取消'],
                maxmin: true, //开启最大化最小化按钮
                area: ['893px', '600px'],
                content:"addForm/?id="+nodeRoot.id+"&&type="+str_type,
                yes:function (index, layero) {

                },
                btn2:function (index, layero) {
                    layer.close()
                }
            });
        }else {
            layer_open(node)
        }

     }


     /**
     左侧树图点击，实时展现右侧树形图数据
     */
    $('#tree').on('nodeSelected', function(event, data) {
        var mode_node;
        Node = data;

        $.ajax({
            url:'shownodes/',
            type:'GET',
            async: false,
            data: {'type': data.tags, 'id': data.id},
            success:function(result){
                $('#tree_mode').treeview({
                    data: result['nodes_failure'],
                    levels:4,
                    expandIcon:"glyphicon glyphicon-plus-sign",
                    collapseIcon:'glyphicon glyphicon-minus-sign',
                });
            }
        })


    // $('#tree_mode').on('nodeSelected', function(event, data){
    //     mode_node = data;
    //     if (data.tags[0] === 'process') {
    //         menu = _processmenu;
    //     }else if ($.inArray(data.tags[0], ['feature', 'variation', 'requirement']) >= 0) {
    //         menu = [
    //             {
    //                 type: "item",
    //                 icon: "chain-broken",
    //                 text: "失效模式",
    //                 key: "pro",
    //                 action: function () {

    //                 }
    //             },
    //             {
    //                 type: "item",
    //                 icon: "bandcamp",
    //                 text: "预防措施",
    //                 key: "pro",
    //                 action: function () {

    //                 }
    //             }]
    //     }
    // })


    /**
    初始化右侧菜单（需要放在函数外面，否则导致参数不修改）
    */
    $('#tree').contextMenu({
        items: _menuItems.concat(_processmenu)
    });


    /**
     * 给定一个node对象初始化成树
     * @param node
     */
    function iniTree(node) {
         node['state'] = {
            checked: true,
            disabled: false,
            expanded: true,
            selected: true
        };
        var json_data= [];
        json_data[0] = node;
        $('#treeview').treeview({
            data: json_data,
            showTags: true,
        });
    }

    /*
    *根据需要找到父节点
    */
    function getParent(node,level){
        var parentNode = $('#tree').treeview('getParent', node);
        for(var i=1; i < level; i++){
            parentNode = $('#tree').treeview('getParent', parentNode);
        };
        return parentNode
    }

    /**
     * 给定一个节点返回根节点
     * @param node
     * @returns
     */
    function getRoot(node) {
        var parentNode = $('#tree').treeview('getParent', node);
        if(parentNode && parentNode.nodes != null ){
            return getRoot(parentNode);
        }else {
            return node;
        }
    };


    // /**
    //  * 初始化右键菜单
    //  * @type {[null,null,null,null,null,null,null,null,null,null,null,null,null]}
    //  * @private
    //  */
    // var _menuItems = [
    // {
    //     type: "title",
    //     text: "Modifica"
    // },
    // {
    //     type: "item",
    //     icon: "clone",
    //     text: "复制",
    //     key: "copy",
    //     action: function () {
    //         layer.open({
    //             type: 2,
    //             content: 'http://layim.layui.com',
    //             area: ['1000px', '500px'],
    //             maxmin: true
    //         });
    //     }
    // },
    // {
    //     type: "item",
    //     icon: "scissors",
    //     text: "剪切",
    //     key: "cut",
    //     action: function () {

    //     }
    // },
    // {
    //     type: "item",
    //     icon: "clipboard",
    //     text: "粘贴",
    //     key: "paste",
    //     action: function () {

    //     }
    // },
    // {
    //     type: "divider"
    // },
    // {
    //     type: "item",
    //     icon: "file-text",
    //     text: "添加",
    //     key: "add",
    //     action: function () {
    //         if(Node==null || Node==undefined){
    //             alert('请选择一个节点！')
    //         }else{
    //             var nodeRoot = getRoot(Node);
    //             layer.open({
    //                 type: 2,
    //                 title: nodeRoot.text,
    //                 id:'myiframe',
    //                 shadeClose: true,
    //                 shade: false,
    //                 btn:['提交', '取消'],
    //                 maxmin: true, //开启最大化最小化按钮
    //                 area: ['893px', '600px'],
    //                 content:"addForm/?id="+nodeRoot.id+"&&Node="+nodeRoot.text,
    //                 yes:function (index, layero) {
    //                     var iframeWin = window[layero.find('iframe')[0]['name']];
    //                     var node = iframeWin.submit();
    //                     $('#tree').treeview({
    //                         data: node['treedata'],
    //                         showTags: true,
    //                         onNodeSelected: function (event, data) {
    //                             iniTree(data);
    //                             Node = data
    //                     }
    //                     });
    //                     var results = $('#tree').treeview('search', [node['text'],{}]);
    //                     var parent = $('#tree').treeview('getParent', results[0]);
    //                     console.log(parent);
    //                     $('#tree').treeview('toggleNodeSelected', [ parent.nodeId, { silent: true } ]);
    //                     iniTree(parent)
    //                 },
    //                 btn2:function (index, layero) {
    //                     layer.close()
    //                 }
    //             });
    //         }
    //     }
    // },
    //     {
    //     type: "item",
    //     icon: "eraser",
    //     text: "删除",
    //     key: "delete",
    //     action: function () {
    //         if(Node == null || Node == undefined){
    //             alert("请选择一个支点")
    //         }else {
    //             var parentNode = $('#tree').treeview('getParent', Node);
    //             var con = confirm("确定删除该支点吗？");
    //             console.log(Node);
    //             if(con == true){
    //                 if($.inArray(Node.text,['失效原因',"过程流程","产品特性","工艺特性",'要求','失效模式','失效影响' ])>=0){
    //                     alert("此支点不允许删除")
    //                 }else {
    //                     $.ajax({
    //                     type: "POST",
    //                     url: "treeData_del/",
    //                     data: {'parentNode':parentNode.text, 'Node': Node.id},
    //                     success: function (data) {
    //                         alert(data);
    //                         $('#tree').treeview('deleteNode',[Node.nodeId]);
    //                     }
    //                 });
    //                 }
    //             }else {
    //                 return false;
    //             }

    //         }
    //     }
    // },
    // {
    //     type: "item",
    //     icon: "pencil",
    //     text: "编辑",
    //     key: "update",
    //     action: function () {
    //         if(Node!=null && Node!=undefined){

    //             if (Node.tags == null || Node.tags == undefined){
    //                 return true
    //             }else {
    //                 alert("该节点不可以编辑");
    //             }

    //         }else {
    //             alert('请选择一个节点！')
    //         }

    //     }
    // },
    //  {
    //     type: "item",
    //     icon: "pencil",
    //     text: "新建",
    //     key: "update",
    //     action: function () {
    //         layer.open({
    //                 type: 2,
    //                 title: "新建数据",
    //                 id:'myiframe',
    //                 shadeClose: true,
    //                 shade: false,
    //                 btn:['提交', '取消'],
    //                 maxmin: true, //开启最大化最小化按钮
    //                 area: ['893px', '600px'],
    //                 content:"newData/",
    //                 yes:function (index, layero) {
    //                     var iframeWin = window[layero.find('iframe')[0]['name']];
    //                     var node = iframeWin.node;
    //                     console.log(node);
    //                     $.ajax({
    //                         type: 'POST',
    //                         url: "treeData_create/",
    //                         data: JSON.stringify({'node': node}),
    //                         success: function(data){
    //                             alert(data);
    //                             layer.closeAll();
    //                         },
    //                         error: function(data){
    //                             return false
    //                         }
    //                     })
    //                 },
    //                 btn2:function (index, layero) {
    //                     layer.close()
    //                 }
    //             });

    //     }
    // },
    // {
    //     type: "submenu",
    //     text: "Condividi con...",
    //     items: [

    //         {
    //             type: "title",
    //             text: "Condividi con..."
    //         },
    //         {
    //             type: "item",
    //             icon: "google-plus-official",
    //             text: "Google+",
    //             key: "google_plus",
    //             action: function () {

    //             }
    //         },
    //         {
    //             type: "item",
    //             icon: "facebook-official",
    //             text: "Facebook",
    //             key: "facebook",
    //             action: function () {

    //             }
    //         },
    //         {
    //             type: "item",
    //             icon: "twitter",
    //             text: "Twitter",
    //             key: "twitter",
    //             action: function () {

    //             }
    //         }
    //     ]
    // },
    // {
    //     type: "divider"
    // },
    // {
    //     type: "title",
    //     text: "Pagina"
    // },
    // {
    //     type: "item",
    //     icon: "refresh",
    //     text: "刷新",
    //     action: function()
    //     {
    //         window.location.reload();
    //     }
    // },
    // {
    //     type: "item",
    //     icon: "home",
    //     text: "Torna alla home",
    //     action: function()
    //     {
    //         window.location.href = "/";
    //     }
    // }
    // ];

    // $(window).contextMenu({

    //     items: _menuItems

    // });
















});
