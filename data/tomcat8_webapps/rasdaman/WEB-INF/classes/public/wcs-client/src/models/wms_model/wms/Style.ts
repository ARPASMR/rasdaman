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

 /**
  * Part of WMS Layer
  */
module wms {
    export class Style {  
        public name:string;
        public abstract:string;
        // 0 is rasql transform fragment, 1 is wcps query fragment
        public queryType:number;
        // query in rasql transform style or wcps query style
        public query:string;

        public constructor(name:string, abstract:string, queryType:number, query:string) {
            this.name = name;
            this.abstract = abstract;
            this.queryType = queryType;
            this.query = query;
        }
    }
}