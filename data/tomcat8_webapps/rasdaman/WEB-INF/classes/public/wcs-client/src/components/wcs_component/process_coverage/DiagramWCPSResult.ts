/*
 * This file is part of rasdaman community.
 *
 * Rasdaman community is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Rasdaman community is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with rasdaman community.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright 2003 - 2017 Peter Baumann /
 rasdaman GmbH.
 *
 * For more information please see <http://www.rasdaman.org>
 * or contact Peter Baumann via <baumann@rasdaman.com>.
 */

///<reference path="../../../common/_common.ts"/>
///<reference path="WCPSQueryResult.ts"/>

module rasdaman {
    export class DiagramWCPSResult extends WCPSQueryResult {
        public diagramData:any;
        public diagramOptions:any;

        public constructor(command:WCPSCommand, data:string) {
            super(command);

            var diagramType = "lineChart";
            if (command.widgetConfiguration.parameters && command.widgetConfiguration.parameters.type) {
                diagramType = command.widgetConfiguration.parameters.type;
            }

            //line
            //column
            //area
            this.diagramOptions = {
                chart: {
                    type: diagramType,
                    height: 300,
                    clipEdge: true,
                    showValues: true,
                    x: function (d) {
                        return d.x;
                    },
                    y: function (d) {
                        return d.y;
                    },
                    transitionDuration: 500,
                    xAxis: {
                        axisLabel: 'X',
                        showMaxMin: false
                    },
                    yAxis: {
                        axisLabel: 'Y',
                        //orient: "bottom",
                        showMaxMin: false,
                        axisLabelDistance: -20
                    }
                }
            };


            // 1D csv, no need to subtract ([ ... ]), json is needed
            if (data.indexOf("[") !== -1) {
                // json
                data = data.substr(1, data.length - 2);
            }
        
            var rawData:number[] = JSON.parse("[" + data  + "]");
            var processedValues = [];
            for (var i = 0; i < rawData.length; ++i) {
                processedValues.push({
                    x: i,
                    y: rawData[i]
                });
            }

            this.diagramData = [
                {
                    values: processedValues
                }
            ];
        }
    }
}
