var menu = [

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
            {
                type: "divider"
            },
            {
                type: "item",
                icon: "hourglass-1",
                text: "产品特性",
                key: "pro",
                action: function () {
                   layer_open(my_node, 'product');
                }
            },
            {
                type: "item",
                icon: "hourglass",
                text: "过程特性",
                key: "proce",
                action: function () {
                    layer_open(my_node, 'variation');
                }
            },
            {
                type: "item",
                icon: "gears",
                text: "要求",
                key: "req",
                action: function () {
                    layer_open(my_node, 'requirement');
                }
            },
            {
                type: "item",
                icon: "chain-broken",
                text: "失效模式",
                key: "pro",
                action: function () {
                    layer_failure(my_node, 'failure');
                }
            },
            {
                type: "item",
                icon: "bandcamp",
                text: "预防措施",
                key: "pro",
                action: function () {

                }
            }
    ]

    /**
     *要求，特性弹出层的函数实现
     */
     function layer_open(node, str_type){
        var process_id = $('#pro_id').val();
        layer.open({
            type: 2,
            title: $('#mode_name').html(),
            id:'myiframe',
            shadeClose: true,
            shade: false,
            btn:['提交', '取消'],
            maxmin: true, //开启最大化最小化按钮
            area: ['893px', '600px'],
            content:"addForm/?id="+process_id+"&type="+str_type,
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

     /**
     失效模式的弹出层实现
     */
     function layer_failure(node, str_type){
        console.log('dddddd');
        var noderoot = getRoot(node);
        url = "addfaliure/?id="+noderoot.id+"&node="+noderoot.tags[0]+"&type="+str_type
        console.log(url);
        layer.open({
            type:2,
            title:noderoot.text,
            shadeClose: true,
            id:'faliureframe',
            shade: false,
            btn:['提交', '取消'],
            maxmin: true, //开启最大化最小化按钮
            area: ['893px', '600px'],
            content: url,
            yes: function(index, layero){
                var iframeWin = window[layero.find('iframe')[0]['name']];
                var failure_modes = iframeWin.failure_modes;
                $.post("addfaliure/",JSON.stringify({'failure_modes': failure_modes}),function(result){
                    alert(result);
                    layer.closeAll();
                });

            },
            btn2: function(index, layero){
                layer.close()
            }
        });
     }

     /**
     * 给定一个node对象初始化成树
     * @param node
     */
    function iniTree(node, tree_type) {
         node['state'] = {
            checked: true,
            disabled: false,
            expanded: true,
            selected: true
        };
        var json_data= [];
        json_data[0] = node;
        $(tree_type).treeview({
            data: json_data,
            showTags: true,
        });
    }

    /*
    *根据需要找到父节点
    */
    function getParent(node,level, tree_type){
        var parentNode = $(tree_type).treeview('getParent', node);
        for(var i=1; i < level; i++){
            parentNode = $(tree_type).treeview('getParent', parentNode);
        };
        return parentNode
    }

    /**
     * 给定一个节点返回根节点
     * @param node
     * @returns
     */
    function getRoot(node, tree_type) {
        var parentNode = $(tree_type).treeview('getParent', node);
        if(parentNode && parentNode.nodes != null ){
            return getRoot(parentNode);
        }else {
            return node;
        }
    };

    // function re_menu(data){
    //     console.log(data);
    //     var my_menu;
    //     if (data !== undefined && data.tags[0] === 'process') {
    //         my_menu = menu.concat(
    //         {
    //             type: "divider"
    //         },
    //         {
    //             type: "item",
    //             icon: "hourglass-1",
    //             text: "产品特性",
    //             key: "pro",
    //             action: function () {
    //                layer_open(my_node, 'product');
    //             }
    //         },
    //         {
    //             type: "item",
    //             icon: "hourglass",
    //             text: "过程特性",
    //             key: "proce",
    //             action: function () {
    //                 layer_open(my_node, 'variation');
    //             }
    //         },
    //         {
    //             type: "item",
    //             icon: "gears",
    //             text: "要求",
    //             key: "req",
    //             action: function () {
    //                 layer_open(my_node, 'requirement');
    //             }
    //         },);
    //         $('#tree_mode').contextMenu({

    //             items: my_menu

    //         });
    //     }else if (data !== undefined && $.inArray(data.tags[0], ['feature', 'variation', 'requirement']) >= 0) {
    //         my_menu = menu.concat({
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
    //             })
    //         $('#tree_mode').contextMenu({

    //             items: my_menu

    //         });
    //     }else{
    //         my_menu = menu
    //         $('#tree_mode').contextMenu({

    //             items: my_menu

    //         });
    //     }
    //     console.log(my_menu)
    //     return my_menu
    // }

    $('#tree_mode').contextMenu({
        items: menu
    });


