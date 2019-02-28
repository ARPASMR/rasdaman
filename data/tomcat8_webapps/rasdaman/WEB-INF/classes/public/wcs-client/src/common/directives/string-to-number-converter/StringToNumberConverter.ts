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

///<reference path="../../../../assets/typings/tsd.d.ts"/>

module rasdaman.common {
    /**
     * Directive used to convert a model from a string to a number for display and from a number to a string for storage back in the model.
     * @returns {{require: string, link: (function(angular.IScope, JQuery, angular.IAttributes, angular.INgModelController): undefined)}}
     * @constructor
     */
    export function StringToNumberConverter():angular.IDirective {
        return {
            require: 'ngModel',
            link: function (scope:angular.IScope, elem:JQuery, attributes:angular.IAttributes, ngModel:angular.INgModelController) {

                ngModel.$parsers.push(function (value) {
                    return '' + value;
                });

                ngModel.$formatters.push(function (value) {
                    return parseFloat(value);
                });
            }
        };
    }
}