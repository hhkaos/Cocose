/*

This file is part of Ext JS 4

Copyright (c) 2011 Sencha Inc

Contact:  http://www.sencha.com/contact

GNU General Public License Usage
This file may be used under the terms of the GNU General Public License version 3.0 as published by the Free Software Foundation and appearing in the file LICENSE included in the packaging of this file.  Please review the following information to ensure the GNU General Public License version 3.0 requirements will be met: http://www.gnu.org/copyleft/gpl.html.

If you are unsure which license is appropriate for your use, please contact the sales department at http://www.sencha.com/contact.

*/
Ext.require(['*']);
Ext.onReady(function() {
    var cw;
    
    Ext.create('Ext.Viewport', {
        layout: {
            type: 'border',
            padding: 5
        },
        defaults: {
            split: true
        },
        dockedItems:createToolbar(),
        items: [{
            region: 'west',
            collapsible: true,
            title: 'Empresas',
            split: true,
            width: '30%',
            minWidth: 100,
            minHeight: 140,
            html: 'west<br>I am floatable',
            dockedItems:createToolbar()
        },{
            region: 'center',
            layout: 'border',
            border: false,
            items: [{
                region: 'center',
                html: 'center center',
                title: 'Previsualización de la web',
                minHeight: 80,
                items: [cw = Ext.create('Ext.Window', {
                    xtype: 'window',
                    closable: false,
                    minimizable: true,
                    title: 'Constrained Window',
                    height: 200,
                    width: 400,
                    constrain: true,
                    html: 'I am in a Container',
                    itemId: 'center-window',
                    minimize: function() {
                        this.floatParent.down('button#toggleCw').toggle();
                    }
                })]
            }]
        },{
            region: 'east',
            collapsible: true,
            floatable: true,
            split: true,
            width: 200,
            minWidth: 120,
            minHeight: 140,
            title: 'East',
            layout: {
                type: 'vbox',
                padding: 5,
                align: 'stretch'
            },
            items: [{
                xtype: 'textfield',
                labelWidth: 70,
                fieldLabel: 'Text field'
            }, {
                xtype: 'component',
                html: 'I am floatable'
            }]
        },{
            region: 'south',
            collapsible: true,
            split: true,
            height: 200,
            minHeight: 120,
            title: 'Personal',
            html: 'Test'
        }]
    });
    
});
/**
 * Creates the toolbar to be used for controlling feeds.
 * @private
 * @return {Ext.toolbar.Toolbar}
 */
createToolbar = function(){
    this.createActions();
    this.toolbar = Ext.create('widget.toolbar', {
        items: [this.addAction, this.removeAction]
    });
    return this.toolbar;
}

/**
 * Create actions to share between toolbar and menu
 * @private
 */
createActions = function(){
    this.addAction = Ext.create('Ext.Action', {
        scope: this,
        handler: this.onAddFeedClick,
        text: 'Add feed',
        iconCls: 'feed-add'
    });

    this.removeAction = Ext.create('Ext.Action', {
        itemId: 'remove',
        scope: this,
        handler: this.onRemoveFeedClick,
        text: 'Remove feed',
        iconCls: 'feed-remove'
    });
}
