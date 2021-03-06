import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

export interface Bar {
  name: string;
  license: string;
  city: string;
  phone: string;
  addr: string;
}

export interface Beer {
  name:string;
}

export interface Drinker {
  name: string;
}

export interface DrinkerBar {
  bar: string;
}

export interface BarMenuItem {
  beer: string;
  manf: string;
  price: number;
}

export interface Transaction {
  drinker: string;
  bar: string;
  total: string;
  tips: string;
  datetime: any;
}

export interface BeerOrder {
  itemname: string;
  quantities: string;
}

export interface BarSpendings {
  bar: string;
  total: string;
}

export interface DrinkerSpending {
  drinker: string;
  total: string;
}

export interface ManfOrder {
  manf: string;
  quantities: string;
}

export interface TotalSale {
  total: string;
  datetime: any;
}

export interface BarOrder {
  bar: string;
  quantities: string;
}

export interface DrinkerOrder {
  drinker: string;
  quantities: string;
}

export interface ItemSale {
  quantities: string;
}

@Injectable({
  providedIn: 'root'
})

@Injectable()
export class BarsService {
  constructor(
    public http: HttpClient
  ) { }

  getBars() {
    return this.http.get<Bar[]>('/api/bar');
  }

  getBar(bar: string) {
    return this.http.get<Bar>('/api/bar/' + bar);
  }

  getMenu(bar: string) {
    return this.http.get<BarMenuItem[]>('/api/menu/' + bar);
  }

  getFrequentCounts() {
    return this.http.get<any[]>('/api/frequents-data');
  }

  getDrinkers() {
    return this.http.get<Drinker[]>('/api/drinker');
  }

  getBarsByDrinker(drinker: string) {
    return this.http.get<DrinkerBar[]>('/api/drinker/bar/' + drinker);
  }

  getTransactionsByDrinker(drinker: string) {
    return this.http.get<Transaction[]>('/api/transaction/' + drinker);
  }

  getTransactionsByDrinkerBar(drinker: string, bar: string) {
    return this.http.get<Transaction[]>('/api/transaction/' + drinker + '/' + bar);
  }

  getBeerOrdersByDrinker(drinker: string, bar: string) {
    return this.http.get<BeerOrder[]>('/api/drinker/beer_orders/' + drinker + "/" + bar);
  }

  getBarSpendingsByDrinker(drinker: string, bar: string, start_date: string, end_date: string) {
    return this.http.get<BarSpendings[]>('/api/drinker/bar_spendings/' + drinker
      + "/" + bar + "/" + start_date + "/" + end_date);
  }

  getDrinkerSpendingsByBar(bar: string) {
    return this.http.get<DrinkerSpending[]>('/api/bar/drinker_spendings/' + bar);
  }

  getBeerOrdersByBar(bar: string) {
    return this.http.get<BeerOrder[]>('/api/bar/beer_orders/' + bar);
  }

  getManfBeerOrdersByBar(bar: string) {
    return this.http.get<ManfOrder[]>('/api/bar/manf_beer_orders/' + bar);
  }

  getBarSales(bar: string, start_date: string, end_date: string) {
    return this.http.get<TotalSale[]>('/api/bar/sales/' + bar + "/" + start_date + "/" + end_date);
  }

  getBeers() {
    return this.http.get<Beer[]>('/api/beer');
  }

  getBeerOrdersForBars(beer: string) {
    return this.http.get<BarOrder[]>('/api/beer/bar_beer_orders/' + beer);
  }

  getBeerOrdersForDrinkers(beer: string) {
    return this.http.get<DrinkerOrder[]>('/api/beer/drinker_beer_orders/' + beer);
  }

  getBeerSales(beer: string, start_date: string, end_date: string) {
    return this.http.get<ItemSale[]>('/api/beer/sales/' + beer + "/" + start_date + "/" + end_date);
  }

  runCustomSql(sqlstr: string) {
    return this.http.get<string>('/api/sql/' + sqlstr);
  }

  readTable(table: string) {
    return this.http.get<any[]>('/api/table/' + table);
  }

  getItemPrice(bar: string, itemtype: string,
    itemname: string, quantities: number) {
    return this.http.get<number>('/api/price/' + bar + '/' + itemtype
      + '/' + itemname + '/' + quantities);
  }

  addBillRec(bar: string, drinker: string, total: number, tips: number, datetime: string) {
    return this.http.get<string>('/api/bill/add/' + bar + '/' + drinker + '/' + total
      + '/' + tips + '/' + datetime);
  }

  addBilldetailRec(bar: string, drinker: string, datetime: string,
    itemtype: string, itemname: string, quantities: number) {
    return this.http.get<string>('/api/billdetail/add/' + bar + '/' + drinker
      + '/' + datetime + '/' + itemtype + '/' + itemname + '/' + quantities);
  }

  addFrequent(bar: string, drinker: string) {
    return this.http.get<string>('/api/frequent/add/' + bar + '/' + drinker);
  }

  addSell(bar: string, itemtype: string, itemname: string, price: number) {
    return this.http.get<string>('/api/sell/add/' + bar + '/' + itemtype + '/' + itemname + '/' + price);
  }
}

/*
export class BarsService {

  constructor() { }
}
*/
