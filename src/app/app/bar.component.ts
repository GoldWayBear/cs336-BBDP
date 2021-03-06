import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BarsService, Bar, Drinker } from '../bars.service';


export interface ItemRec {
  name: string;
  manf: string;
}

export interface BillDetail {
  itemname: string;
  itemtype: string;
  quantities: number;
}

@Component({
  selector: 'app-bar',
  templateUrl: './bar.component.html',
  styleUrls: ['./bar.component.css']
})
export class BarComponent implements OnInit {

  bars: Bar[];
  selectedBar: string;

  // add transactions
  drinkers: Drinker[];
  selectedDrinker: string;
  selectedItemtype: string;
  selectedItemname: string;
  items: ItemRec[];
  billdetails: BillDetail[];
  totalPrice: number = 0.0;

  // CHART OPTIONS.
  chartOptions = {
    responsive: true    // THIS WILL MAKE THE CHART RESPONSIVE (VISIBLE IN ANY DEVICE).
  }

  // drinker spendings chart
  drinkerSpendingsLabels: string[];
  drinkerSpendingsData = [
    {
      label: 'Drinker Spendings',
      data: []
    }
  ];
  drinkerSpendingsColors = [
    {
      backgroundColor: 'rgba(30, 169, 224, 0.8)'
    }
  ];

  // beer orders chart
  beerOrdersLabels: string[];
  beerOrdersData = [
    {
      label: 'Beer Orders',
      data: []
    }
  ];
  beerOrdersColors = [
    {
      backgroundColor: 'rgba(30, 169, 224, 0.8)'
    }
  ];

  // manufactures chart
  manfOrdersLabels: string[];
  manfOrdersData = [
    {
      label: 'Manufacture Beer Orders',
      data: []
    }
  ];
  manfOrdersColors = [
    {
      backgroundColor: 'rgba(30, 169, 224, 0.8)'
    }
  ];


  // bar sales chart
  // ????????????????


  constructor(
    private barService: BarsService,
    private route: ActivatedRoute) { }

  ngOnInit() {
    this.getBars();
  }

  filterBar(bar: any) {
    //alert("selected:"+bar)
    this.selectedBar = "0";
    this.drinkerSpendingsLabels = [];
    this.drinkerSpendingsData[0].data = [];
    this.beerOrdersLabels = [];
    this.beerOrdersData[0].data = [];
    this.manfOrdersLabels = [];
    this.manfOrdersData[0].data = [];
    this.drinkers = [];
    this.selectedDrinker = "";
    if (bar == "0") {
      // don't populate charts
    } else {
      this.selectedBar = bar;
      this.getDrinkerSpendingsByBar(this.selectedBar);
      this.getBeerOrdersByBar(this.selectedBar);
      this.getManfBeerOrdersByBar(this.selectedBar);
/*
      let start_date = document.getElementById('start').value;
      //alert("Start date:"+start_date);
      let end_date = document.getElementById('end').value;
      //alert("End date:"+end_date);
      this.getBarSales(this.selectedBar, start_date, end_date);
*/
      //alert("getDrinkers!");
      this.getDrinkers();
    }
  }

  filterDinker(drinker: any) {
    this.selectedDrinker = drinker;
    this.billdetails = [];
    this.selectedItemname = "";
    this.selectedItemtype = "";
    this.items = [];
  }

  filterItemType(itemtype: any) {
    this.selectedItemtype = itemtype;
    this.items = [];
    this.selectedItemname = "";
    let table = "";
    if (itemtype == "food")
      table = "food";
    else if (itemtype == "beer")
      table = "beers";
    else if (itemtype == "soft drink")
      table = "softdrinks";
    this.readTable(table);
  }

  filterItemName(itemname: any) {
    this.selectedItemname = itemname;
  }

  addItemToBilldetail() {
    let billdetail = {
      itemname: this.selectedItemname,
      itemtype: this.selectedItemtype,

      quantities: +(<HTMLInputElement>document.getElementById('quantity')).value

    };
    //alert("billdetail:"+billdetail);
    this.billdetails.push(billdetail);
    //alert("billdetails:"+this.billdetails);
    //alert("total:"+this.getBillTotal(billdetail))
    this.getBillTotal(billdetail);
    (<HTMLInputElement>document.getElementById('total')).value = ""+this.totalPrice;
  }

  newBill() {
    this.drinkers = [];
    this.selectedDrinker = "";
    this.selectedItemtype = "";
    this.selectedItemname = "";
    this.items = [];
    this.billdetails = [];
    this.totalPrice = 0.0;

    (<HTMLInputElement>document.getElementById('total')).value = "0.0";

    (<HTMLInputElement>document.getElementById('tips')).value = "0.0";

    this.getDrinkers();
  }

  addBill() {
    // Note: should use DB transaction, but not due to limited development time
    this.addBillRec();

    for (let i = 0; i < this.billdetails.length; i++) {
      this.addBilldetailRec(this.billdetails[i]);
    }
  }

  getBars() {
      this.barService.getBars().subscribe(
        data => {
          this.bars = data;
        },
        error => {
          alert('Could not retrieve a list of bars');
        }
      );
  }

  getDrinkers() {
      this.barService.getDrinkers().subscribe(
        data => {
          this.drinkers = data;
          //alert("drinkers:"+data);
        },
        error => {
          alert('Could not retrieve a list of drinkers');
        }
      );
  }

  getDrinkerSpendingsByBar(bar: string) {
      this.barService.getDrinkerSpendingsByBar(bar).subscribe(
        data => {
          let len = data.length;
          this.drinkerSpendingsLabels = [];
          for (let i = 0; i < len; i++) {
            this.drinkerSpendingsLabels.push(data[i].drinker);
            this.drinkerSpendingsData[0].data.push(data[i].total);
          }
        },
        error => {
          alert('Could not retrieve a list of drink spendings');
        }
      );
  }

  getBeerOrdersByBar(bar: string) {
      this.barService.getBeerOrdersByBar(bar).subscribe(
        data => {
          let len = data.length;
          this.beerOrdersLabels = [];
          for (let i = 0; i < len; i++) {
            this.beerOrdersLabels.push(data[i].itemname);
            this.beerOrdersData[0].data.push(data[i].quantities);
          }
        },
        error => {
          alert('Could not retrieve a list of beer orders');
        }
      );
  }

  getManfBeerOrdersByBar(bar: string) {
      this.barService.getManfBeerOrdersByBar(bar).subscribe(
        data => {
          let len = data.length;
          this.manfOrdersLabels = [];
          for (let i = 0; i < len; i++) {
            this.manfOrdersLabels.push(data[i].manf);
            this.manfOrdersData[0].data.push(data[i].quantities);
          }
        },
        error => {
          alert('Could not retrieve a list of manufacture orders');
        }
      );
  }

  getBarSales(bar: string, start_date: string, end_date: string) {
    this.barService.getBarSales(bar, start_date, end_date).subscribe(
      data => {
        let len = data.length;

        // ????????????????????????????
/*
        this.barSalesLabels = [];
        for (let i = 0; i < len; i++) {
          this.barSalesLabels.push(data[i].datetime);
          this.barSalesData[0].data.push(data[i].total);
        }
*/
      },
      error => {
        alert('Could not retrieve a list of bar sales: '+error.message);
      }
    );
  }

  readTable(table: string) {
    this.barService.readTable(table).subscribe(
      data => {
        this.items = data;
      },
      error => {
        alert('Could not read table: '+error.message);
      }
    );
  }

  getBillTotal(billdetail) {
    //let preTotal: number = +document.getElementById('total').value;
    //alert("getBillTotal preTotal:"+preTotal)
    //let price: number = 0.0;
    this.barService.getItemPrice(this.selectedBar, billdetail.itemtype,
      billdetail.itemname, billdetail.quantities).subscribe(
        data => {
          //alert("getBillTotal db return:"+data)
          //alert("getBillTotal this.totalPrice:"+this.totalPrice)
          let price: number = +data;
          this.totalPrice = this.totalPrice + price;
          //alert("getBillTotal this.totalPrice:"+this.totalPrice)

          (<HTMLInputElement>document.getElementById('total')).value = ""+this.totalPrice;
        },
        error => {
          alert('Could not get item price: '+error.message);
        }
      );
    //let total: number = preTotal + price;
    //alert("getBillTotal total:"+total)
    //return total;
  }

  addBillRec() {
    let total: number = +(<HTMLInputElement>document.getElementById('total')).value;

    let tips: number = +(<HTMLInputElement>document.getElementById('tips')).value;

    let datetime: string = (<HTMLInputElement>document.getElementById('bill_time')).value;

    this.barService.addBillRec(this.selectedBar, this.selectedDrinker,
      total, tips, datetime).subscribe(
        data => {
          if (data != "") {
            alert("Adding a bill: "+data)
          } else {
            alert("A new bill has been added.")
          }

        },
        error => {
          alert('Could not add a bill record: '+error.message);
        }
      );
  }

  addBilldetailRec(billdetail: BillDetail) {

    let datetime: string = (<HTMLInputElement>document.getElementById('bill_time')).value;

    this.barService.addBilldetailRec(this.selectedBar, this.selectedDrinker,
      datetime, billdetail.itemtype, billdetail.itemname,
      billdetail.quantities).subscribe(
        data => {
          //alert("addBilldetailRec db return:"+data)
          if (data == "") {
            alert("A new bill detail has been added.")
          }
        },
        error => {
          alert('Could not add a billdetail record: '+error.message);
        }
      );
  }

}
