/*
 *               jQuery ContextMenu v. 1.0.0
 *
 *                Written by Bilotta Matteo.
 *
 *     Copyright © 2017, Bylothink. All rights reserved.
 */

// Checking if jQuery is available...
    if (typeof(jQuery) === "undefined")
    {
        throw new Error("jQuery is required by ContextMenu to be executed.");
    }
    else if (typeof(Tether) === "undefined")
    {
        throw new Error("Tether is required by ContextMenu to be executed.");
    }

(function(jQuery, Tether, window)
{
    "use strict";

    // Single instance private constants:
        const DEFAULT_OPTS = {

            items: [ ]
        };
        
        const PREFIX = "cnxt-";
        const CURSOR_ID = PREFIX + "cursor";

        const ATTACHMENTS = {
            
            MAIN_MENU: "bottom left",
            SUB_MENU: "top right"
        };

    // Single instance private properties:
        var _context;
        var _contextMenu;
        var _cursor;
        
    // Instance indipendent private methods:
        var _append = function(obj)
        {
            jQuery("body").append(obj);
        };

        var _init = function()
        {
            _context = jQuery(window);
            _cursor = jQuery('<div id="' + CURSOR_ID + '"></div>');

            _append(_cursor);
        };

        var _isUndefined = function(obj)
        {
            return ((obj === undefined) || (typeof(obj) === "undefined"));
        };

        var _onCloseEvent = function()
        {
            if (_isUndefined(_contextMenu) === false)
            {
                _contextMenu.close();
            }
        };

        var _updateCursor = function(e)
        {   
            _cursor.css({ left: e.pageX, top: e.pageY });
        };

    // Classes:
        var Item = function(properties, subMenu)
        {
            // Private properties:
                var _this = this;
                var _subMenu = subMenu;

                var _jQueryObject;

            // Private methods:
                var _enableEvents = function()
                {
                    if (properties.type === "item")
                    {
                        _jQueryObject.on("click", _onClick);
                    }
                    else if (properties.type === "submenu")
                    {
                        _jQueryObject.on("mouseenter", _onMouseEnter);
                        _jQueryObject.on("mouseleave", _onMouseLeave);
                    }
                };
                
                var _init = function()
                {
                    _jQueryObject = _render();
                    
                    _append(_jQueryObject);
                    _enableEvents();
                };
                
                var _onClick = function(e)
                {
                    if (_isUndefined(properties.action) === false)
                    {
                        var _haveToClose = properties.action.call(this, properties);

                        if (_haveToClose !== false)
                        {
                            _contextMenu.close();
                        }
                    }

                    e.preventDefault();
                    e.stopPropagation();
                };

                var _onMouseEnter = function(e)
                {
                    _subMenu.open();
                    
                    e.preventDefault();
                    e.stopPropagation();
                };
                var _onMouseLeave = function(e)
                {
                    _subMenu.close();
                    
                    e.preventDefault();
                    e.stopPropagation();
                };
                
                var _render = function()
                {
                    var _item = jQuery('<li></li>');

                    if (properties.type === "title")
                    {
                        _item.addClass("dropdown-header");
                        _item.html(properties.text);
                    }
                    else if (properties.type === "divider")
                    {
                        _item.addClass("divider");
                        _item.attr("role", "separator");
                    }
                    else if ((properties.type === "item") || (properties.type === "submenu"))
                    {
                        var _link = jQuery('<a></a>');
                        var _innerHtml = properties.text;

                        if (_isUndefined(properties.icon) === false)
                        {
                            _innerHtml = '<span class="fa fa-' + properties.icon + '"></span> ' + _innerHtml;
                        }

                        _link.html(_innerHtml);

                        if (properties.type === "submenu")
                        {
                            _link.addClass("dropdown-toggle");
                            _item.addClass("dropdown-submenu");
                        }

                        _item.append(_link);
                    }

                    return _item;
                };

            // Public methods:
                _this.getJQueryObject = function()
                {
                    return _jQueryObject;
                };

            // Initializing object...
                _init();
        };

        var Menu = function(items)
        {
            // Private properties:
                var _this = this;

                var _items = [];
                var _subMenus = [];

                var _isMainMenu;
                var _jQueryObject;
                var _jQueryTargetObject;
                var _tetherInstance;

            // Private methods:
                var _init = function()
                {
                    _jQueryObject = _render();

                    _append(_jQueryObject);
                };
                
                var _onMouseEnter = function(e)
                {
                    _this.open();
                    
                    e.preventDefault();
                    e.stopPropagation();
                };
                var _onMouseLeave = function(e)
                {
                    _this.close();
                    
                    e.preventDefault();
                    e.stopPropagation();
                };

                var _render = function()
                {
                    var _menu = jQuery('<ul class="context-menu dropdown-menu"></ul>');

                    for (var i in items)
                    {
                        var _item;

                        if (items[i].type === "submenu")
                        {
                            var _subMenu = new Menu(items[i].items);
                            
                            _item = new Item(items[i], _subMenu);

                            _subMenu.enableEvents(_item.getJQueryObject());
                            _subMenus.push(_subMenu);
                        }
                        else
                        {
                            _item = new Item(items[i]);
                        }

                        _items.push(_item);
                        
                        _menu.append(_item.getJQueryObject());
                    }

                    return _menu;
                };

            // Public methods:
                _this.close = function()
                {
                    _jQueryObject.removeClass("open");
                    
                    for (var i in _subMenus)
                    {
                        _subMenus[i].close();
                    }

                    if (_isMainMenu === true)
                    {
                        setTimeout(_this.devare, 150);
                    }
                };
                
                _this.devare = function()
                {
                    _jQueryObject.remove();
                    
                    for (var i in _subMenus)
                    {
                        _subMenus[i].devare();
                    }
                };

                _this.enableEvents = function(target)
                {
                    var _attachment;

                    if (_isUndefined(target) === false)
                    {
                        _attachment = ATTACHMENTS.SUB_MENU;
                        _isMainMenu = false;
                        _jQueryTargetObject = target;
                    }
                    else
                    {
                        _attachment = ATTACHMENTS.MAIN_MENU;
                        _isMainMenu = true;
                        _jQueryTargetObject = _cursor;
                    }

                    _tetherInstance = new Tether({

                        element: _jQueryObject,
                        target: _jQueryTargetObject,
                        attachment: 'top left',
                        targetAttachment: _attachment,
                        constraints: [

                            {
                                attachment: "together",
                                pin: true,
                                to: "window"
                            }
                        ],
                        targetOffset: "0px 0px"
                    });

                    if (_isMainMenu === false)
                    {
                        _jQueryObject.on("mouseenter", _onMouseEnter);
                        _jQueryObject.on("mouseleave", _onMouseLeave);
                    }
                };

                _this.getJQueryObject = function()
                {
                    return _jQueryObject;
                };

                _this.open = function()
                {
                    _jQueryObject.addClass("open");
                    _tetherInstance.position();
                };

            // Initializing object...
                _init();
        };

        var ContextMenu = function(domElements, options)
        {
            // Private properties:
                var _this = this;
                var _domElements = domElements;

                var _items = options.items;
            
            // Private methods:
                var _onRightClick = function(e)
                {
                    if (_isUndefined(_contextMenu) === false)
                    {
                        _contextMenu.close();
                    }

                    _updateCursor(e);

                    var _computedItems = _items;

                    if (typeof(_items) === "function")
                    {
                        _computedItems = _items.call(this);
                    }

                    _contextMenu = new Menu(_computedItems);
                    _contextMenu.enableEvents();
                    _contextMenu.open();

                    e.preventDefault();
                    e.stopPropagation();
                };

            // Start listening for events...
                jQuery(_domElements).on("contextmenu", _onRightClick);
        };

    // Initial initialization...
        _init();

        // Start listening for global events...
            _context.on("click", _onCloseEvent);
            _context.on("contextmenu", _onCloseEvent);

    // Exposing ContextMenu as a jQuery plugin...
        jQuery.fn.contextMenu = function(options)
        {
            if (_isUndefined(this) === false)
            {
                var _opts = jQuery.extend({ }, DEFAULT_OPTS, options);

                return new ContextMenu(this, _opts);
            }
        };

})(jQuery, Tether, window);
