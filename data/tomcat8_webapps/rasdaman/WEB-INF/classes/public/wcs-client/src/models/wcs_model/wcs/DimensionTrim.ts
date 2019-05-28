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

///<reference path="DimensionSubset.ts"/>

module wcs {
    export class DimensionTrim extends DimensionSubset {
        public trimLow:string;
        public trimHigh:string;
        public trimLowNotValid:boolean;
        public trimHighNotValid:boolean;
        public trimLowerUpperBoundNotInOrder:boolean;
        public typeOfTrimUpperNotValidDate:boolean;
        public typeOfTrimLowerNotValidDate:boolean;
        public typeOfTrimUpperNotValidNumber:boolean;
        public typeOfTrimLowerNotValidNumber:boolean;

        public constructor(dimension:string, trimLow?:string, trimHigh?:string) {
            super(dimension);

            this.trimLow = trimLow;
            this.trimHigh = trimHigh;
            this.trimHighNotValid = false;
            this.trimLowNotValid = false;
            this.trimLowerUpperBoundNotInOrder = false;
            this.typeOfTrimLowerNotValidDate = false;
            this.typeOfTrimLowerNotValidNumber = false;
            this.typeOfTrimUpperNotValidDate = false;
            this.typeOfTrimUpperNotValidNumber = false;
        }

        public toKVP():string {
            return this.dimension + "(" + this.trimLow + "," + this.trimHigh + ")";
        }
    }
}