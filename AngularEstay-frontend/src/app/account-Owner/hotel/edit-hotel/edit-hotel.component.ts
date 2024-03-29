import { Component, OnInit } from "@angular/core";
import { GuestService } from "src/app/service/guest.service";
import { ActivatedRoute, Router } from "@angular/router";
import { FormControl } from "@angular/forms";
import { OwnerService } from "src/app/service/owner.service";
import { Observable } from "rxjs";
import { map, startWith } from "rxjs/operators";
import { HttpHeaders } from "@angular/common/http";
import { Hotel } from "src/app/model/hotel.model";

@Component({
  selector: "app-edit-hotel",
  templateUrl: "./edit-hotel.component.html",
  styleUrls: ["./edit-hotel.component.css"]
})
export class EditHotelComponent implements OnInit {
  public hotel: any;
  public property: any;
  public utilities: any;
  public formEdit: any;
  private cities: any;
  public option: string;
  public myControl = new FormControl();
  public filteredOptions: Observable<string[]>;
  private temp: any;
  public errorMessage: string;
  public submitted = false;
  public img?: string;
  public name?: string;
  public address?: string;
  public price?: string;
  public rating?: string;
  public city?: string;

  constructor(
    private guestService: GuestService,
    private activatedRouteService: ActivatedRoute,
    private ownerService: OwnerService,
    private routerService: Router
  ) {}
  headerConfig = {
    headers: new HttpHeaders({
      "user-access-token": window.localStorage.getItem("AuthToken")
    })
  };
  async ngOnInit() {
    this.hotel = new Hotel();
    this.getHotel();

    this.cities = await this.guestService.getAllCities().toPromise();
    this.cities = this.cities.response;

    this.filteredOptions = this.myControl.valueChanges.pipe(
      startWith(""),
      map(value => this._filter(value))
    );
  }

  // Filter input
  public _filter(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.cities.filter(option =>
      option.toLowerCase().includes(filterValue)
    );
  }

  // Get City Name from input
  onOptionSelected(dataOption: any) {
    this.city = dataOption.option.value;
  }

  getHotel() {
    this.activatedRouteService.params.subscribe(data => {
      let id = data.id;
      this.guestService.getOneHotel(id).subscribe(result => {
        this.hotel = result;
        this.property = this.hotel.response.detail_hotels;
        this.name = this.property.name;
        this.address = this.property.address;
        this.city = this.property.city;
        this.img = this.property.img;
        this.price = this.property.price;
        this.rating = this.property.rating;
        this.utilities = this.hotel.response.utilities;
        if (this.property.img == "") {
          this.img = "null";
        } else {
          this.img = this.property.img;
        }
      });
    });
  }

  onSubmit() {
    this.submitted = true;
    this.activatedRouteService.params.subscribe(data => {
      this.hotel.name = this.name;
      this.hotel.address = this.address;
      this.hotel.city = this.city;
      this.hotel.link = "";
      this.hotel.price = this.price;
      this.hotel.rating = this.rating;
      this.hotel.img = this.img;
      if (
        this.hotel.name != null &&
        this.hotel.address != null &&
        this.hotel.city != null &&
        this.hotel.price != null &&
        this.hotel.price > 99999 &&
        this.hotel.price < 9999999 &&
        this.hotel.rating != null &&
        this.hotel.rating > 0 &&
        this.hotel.rating < 11
      ) {
        this.ownerService
          .updateHotel(
            this.hotel.response.detail_hotels.id,
            this.hotel.name,
            this.hotel.address,
            this.hotel.city,
            this.hotel.link,
            this.hotel.img,
            this.hotel.rating,
            this.hotel.price,
            this.hotel.status,
            this.headerConfig
          )
          .subscribe(data => {
            this.temp = data;
            console.log(data);
            if (this.temp.status == 400) {
              this.errorMessage = this.temp.response.error;
            }
            if (this.temp.status == 200) {
              this.routerService.navigate(["host/hotel/all-hotel"]);
            }
          });
      }
    });
  }
}
