namespace my.bookshop;

using { managed } from '@sap/cds/common';

entity Books : managed {
  key ID      : UUID; 
  title       : String(100);
  category    : String(30);
  price       : Decimal(10,2);
  currency    : String(3);
  
  stock       : Integer;
  status      : String(10);
  releaseDate : Date; 
}