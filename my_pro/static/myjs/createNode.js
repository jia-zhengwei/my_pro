$(document).ready(function () {
    var Node;

    /**
     * 查询到输入框内的数据
     * @returns {code: (*|jQuery), name: (*|jQuery)}{boolean}
     */
    function getPro() {
        var code = $("#process_code").val();
        var pro_name = $("#process").val();
        var pro_flow = $('#flow').val();
        if (code == null || pro_name == null){
            alert('输入不能为空！')
        }else {
            var pro = {'code': code, 'name': pro_name, 'flow': pro_flow};
            $('#process_code').val('');
            $('#process').val('');
            return pro
        }
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


    /*
    *初始化树
    */
    function iniTree(node){
        $('#tree').treeview({
                data:node,
                showTags:true,
                onNodeSelected: function (event, data) {
                    var parentNode = $('#tree').treeview('getParent', data);
                    if($.inArray(parentNode.text,['失效原因',"过程流程","产品特性","工艺特性",'要求','失效模式','失效影响' ])>=0){
                        var menu = [
                            {type: "title",text: "Modifica"},
                            {type: "item",icon: "eraser",text: "删除",key: "cut",
                                action: function () {
                                    if(data == null || data == undefined){
                                        alert("请选择一个支点")
                                    }else {
                                        var con = confirm("确定删除该支点吗？");
                                        console.log(data);
                                        if(con == true){
                                            delNode(node,data)
                                            $('#tree').treeview('deleteNode',[data.nodeId]);
                                            console.log(node)
                                        }else {
                                            return false;
                                        }
                                    }
                                }
                            },
                            {type: "item",icon: "pencil",text: "编辑",key: "paste",action: function () {}}
                        ]
                    }else{
                        var menu = [{
                                type: "item",
                                icon: "file-text",
                                text: "添加",
                                key: "copy",
                                action: function () {
                                    var parentNode = $('#tree').treeview('getParent', node);
                                    if(data == null || data == undefined){
                                        alert("请选择一个支点")
                                    }else {
                                        layer.prompt({title: '输入数据', formType: 0}, function(text, index){
                                            layer.close(index);
                                            addNode(node, data, text);
                                        });
                                    }
                                }
                            },
                        ]
                    }
                    $(window).contextMenu({
                        items: menu
                    });
                }
            })
    }

    /**
     * 输入过程后，展现树图
     */
    $('button').click(function () {
        //获取值必须在函数体内
        var pro = getPro();
        if (pro){
            var prodict = {'text': '', 'tags': [], 'nodes': [
                {'text': '产品特性', 'nodes': []},
                {'text': '要求', 'nodes': []},
            ]};
            prodict['text']= pro['code'];
            prodict['tags'].push(pro['name']);
            prodict['tags'].push(pro['flow']);
            node.push(prodict);
            iniTree(node);
        }else {
            return false
        }
    });


    /**
    *删除树的节点，返回新的nodes数据
    */
    function delNode(nodes, node){
        var parentNode = $('#tree').treeview('getParent', [node.nodeId]);
        var rootNode = getRoot(node);
        $.each(nodes,function(index, value){
            if (value['text'] === rootNode.text){
                if (parentNode.text === '产品特性'){
                    nodes[index]['nodes'][0]['nodes'].splice($.inArray(node, nodes[index]['nodes'][0]['nodes']),1)
                }else if (parentNode.text === '工艺特性'){
                    $.each(nodes[index]['nodes'][0]['nodes'],function(index_fir,value_fir){
                        var parent = getParent(node,2)
                        if (value_fir['text'] === parent.text){
                            var arrlist = nodes[index]['nodes'][0]['nodes'][index_fir]['nodes'][0]['nodes']
                            arrlist.splice($.inArray(node, arrlist),1)
                        }
                    })
                }else if (parentNode.text === '要求'){
                    nodes[index]['nodes'][1]['nodes'].splice($.inArray(node, nodes[index]['nodes'][1]['nodes']),1)
                }else if (parentNode.text === '失效模式'){
                    $.each(nodes[index]['nodes'][1]['nodes'], function(index_fir,value_fir){
                        var parent = getParent(node,2)
                        if (value_fir['text'] === parent.text){
                            var arrlist = nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes']
                            arrlist.splice($.inArray(node, arrlist),1)
                        }
                    })
                }else if (parentNode.text === '失效原因'){
                    $.each(nodes[index]['nodes'][1]['nodes'],function(index_fir,value_fir){
                        var parent = getParent(node,4)
                        if (value_fir['text'] === parent.text){
                            $.each(nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'],function(index_sec, value_sec){
                                var parent_sec = getParent(node,2)
                                if (value_sec['text'] === parent_sec.text){
                                    var arrlist = nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'][index_sec]['nodes'][0]['nodes']
                                    arrlist.splice($.inArray(node, arrlist),1)
                                }
                            })
                        }
                    })
                }else if (node.text === '失效影响') {
                    var parent = getParent(node,4)
                    $.each(nodes[index]['nodes'][1]['nodes'],function(index_fir,value_fir){
                        if (value_fir['text'] === parent.text){
                            $.each(nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'],function(index_sec, value_sec){
                                 var parent_sec = getParent(node,2)
                                if (value_sec['text'] === parent_sec.text){
                                    var arrlist = nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'][index_sec]['nodes'][1]['nodes']
                                    arrlist.splice($.inArray(node, arrlist),1)
                                }
                            })
                        }
                    })
                }
            }
        });
    }
    /**
    *树的层级添加
    param:nodes: 节点数组 node:节点
    */
    function addNode(nodes,node,text){
        var parentNode = $('#tree').treeview('getParent', [node.nodeId]);
        var rootNode = getRoot(node);
        $.each(nodes,function(index, value){
            if (value['text'] === rootNode.text){
                if (node.text === '产品特性'){
                    var pro = {'text':text, 'nodes':[{'text':'工艺特性', 'nodes':[]}]};
                    nodes[index]['nodes'][0]['nodes'].push(pro)
                    iniTree(nodes);
                }else if (node.text === '工艺特性'){
                    var pro_node = {'text':text}
                    $.each(nodes[index]['nodes'][0]['nodes'],function(index_fir,value_fir){
                        if (value_fir['text'] === parentNode.text){
                            nodes[index]['nodes'][0]['nodes'][index_fir]['nodes'][0]['nodes'].push(pro_node)
                            iniTree(nodes);
                        }
                    })
                }else if (node.text === '要求'){
                    var req = {'text':text,'nodes':[{'text':'失效模式', 'nodes':[]}]};
                    nodes[index]['nodes'][1]['nodes'].push(req)
                    iniTree(nodes);
                }else if (node.text === '失效模式'){
                    var mode = {'text': text, 'nodes':[{'text':'失效原因', 'nodes':[]},{'text':'失效影响', 'nodes':[]}]}
                    $.each(nodes[index]['nodes'][1]['nodes'], function(index_fir,value_fir){
                        if (value_fir['text'] === parentNode.text){
                            nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'].push(mode)
                            iniTree(nodes);
                        }
                    })
                }else if (node.text === '失效原因'){
                    var cause = {'text':text}
                    var parent = getParent(node,3)
                    console.log(parent)
                    $.each(nodes[index]['nodes'][1]['nodes'],function(index_fir,value_fir){
                        if (value_fir['text'] === parent.text){
                            $.each(nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'],function(index_sec, value_sec){
                                if (value_sec['text'] === parentNode.text){
                                    nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'][index_sec]['nodes'][0]['nodes'].push(cause)
                                    iniTree(nodes);
                                }
                            })
                        }
                    })
                }else if (node.text === '失效影响') {
                    var effect = {'text':text}
                    var parent = getParent(node,3)
                    $.each(nodes[index]['nodes'][1]['nodes'],function(index_fir,value_fir){
                        if (value_fir['text'] === parent.text){
                            $.each(nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'],function(index_sec, value_sec){
                                if (value_sec['text'] === parentNode.text){
                                    nodes[index]['nodes'][1]['nodes'][index_fir]['nodes'][0]['nodes'][index_sec]['nodes'][1]['nodes'].push(effect)
                                    iniTree(nodes);
                                }
                            })
                        }
                    })
                }
            }
        });
        $('#tree').treeview('search', [text,{}]);
    }

    /**
     * 初始化右键菜单
     * @type {[null,null,null,null,null,null,null,null,null,null,null,null,null]}
     * @private
     */
    // var _menuItems = [
    // {
    //     type: "title",
    //     text: "Modifica"
    // },
    // {
    //     type: "item",
    //     icon: "file-text",
    //     text: "添加",
    //     key: "copy",
    //     action: function () {
    //         var parentNode = $('#tree').treeview('getParent', node);
    //         if(Node == null || Node == undefined){
    //             alert("请选择一个支点")
    //         }else {
    //             if($.inArray(parentNode.text,['失效原因',"过程流程","产品特性","工艺特性",'要求','失效模式','失效影响' ])>=0){
    //                     alert("此支点不允许添加")
    //             }
    //             layer.prompt({title: '输入数据', formType: 0}, function(text, index){
    //                 layer.close(index);
    //                 addNode(node, Node, text);
    //             });
    //         }
    //     }
    // },
    // {
    //     type: "item",
    //     icon: "eraser",
    //     text: "删除",
    //     key: "cut",
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
    //     key: "paste",
    //     action: function () {

    //     }
    // }];

    // $(window).contextMenu({

    //     items: _menuItems

    // });


























});
