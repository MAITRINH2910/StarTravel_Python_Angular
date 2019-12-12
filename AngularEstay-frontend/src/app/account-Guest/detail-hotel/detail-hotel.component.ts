import { Component, OnInit } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { Hotel } from "./../../model/hotel.model";
import { GuestService } from "src/app/service/guest.service";
import { UserService } from "src/app/service/user.service";
import { HttpHeaders } from "@angular/common/http";
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { MatDialog } from "@angular/material/dialog";
import { LoginModalComponent } from "../login-modal/login-modal.component";
import { TokenStorageService } from "src/app/service/token-storage.service";
import { RemindFormReviewComponent } from "../remind-form-review/remind-form-review.component";
import { BookingModalComponent } from "../booking-modal/booking-modal.component";

@Component({
  selector: "app-detail-hotel",
  templateUrl: "./detail-hotel.component.html",
  styleUrls: ["./detail-hotel.component.css"]
})
export class DetailHotelComponent implements OnInit {
  public hotel: any;
  public property: any;
  public utilities: any;
  public haveUtility = [];
  public feedback: any;
  public averageRating: number;
  public reviewNumber: number;
  public sum = 0;
  public ratingValue: number;
  public formFeedback: FormGroup;
  public authority: string;
  public role: string;

  headerConfig = {
    headers: new HttpHeaders({
      "user-access-token": window.localStorage.getItem("AuthToken")
    })
  };

  constructor(
    private guestService: GuestService,
    private activatedRouteService: ActivatedRoute,
    private userService: UserService,
    private formBuilder: FormBuilder,
    private dialog: MatDialog,
    private tokenStorage: TokenStorageService
  ) {}
  rating(event) {
    this.ratingValue = event.value;
  }
  ngOnInit() {
    this.hotel = new Hotel();
    this.getHotel();
    this.activatedRouteService.params.subscribe(data => {
      let id = data.id;
      this.userService.getAllFeedback(id).subscribe(data => {
        this.feedback = data;
        this.feedback = this.feedback.response;
        this.reviewNumber = this.feedback.length;
        this.feedback.forEach(item => {
          this.sum = this.sum + item.rating;
        });
        if (this.feedback.length != 0) {
          this.averageRating = this.sum / this.feedback.length;
        } else {
          this.averageRating = null;
        }
      });
    });
    this.form();
    if (window.localStorage.getItem("AuthToken") != null) {
      this.role = this.tokenStorage.getAuthority();
    }
  }

  getHotel() {
    this.activatedRouteService.params.subscribe(data => {
      let id = data.id;
      this.guestService.getOneHotel(id).subscribe(result => {
        this.hotel = result;
        this.property = this.hotel.response.detail_hotels;
        this.utilities = this.hotel.response.utilities;
        for (let utility in this.utilities) {
          let value = this.utilities[utility];
          if (value == 1) {
            this.haveUtility.push(utility);
          }
        }
      });
    });
  }

  form() {
    this.formFeedback = this.formBuilder.group({
      comment: ["", [Validators.required]]
    });
  }
  onSubmit() {
    if (
      window.localStorage.getItem("AuthToken") == null ||
      this.role != "USER"
    ) {
      this.dialog.open(LoginModalComponent);
    }
    if (
      this.ratingValue != undefined &&
      this.formFeedback.value.comment != ""
    ) {
      this.activatedRouteService.params.subscribe(data => {
        let hotel_id = data.id;
        this.userService
          .addFeedback(
            hotel_id,
            this.formFeedback.value.comment,
            this.ratingValue,
            this.headerConfig
          )
          .subscribe(data => {
            window.location.reload();
          });
      });
    }
    if (
      (this.role == "USER" && this.ratingValue == undefined) ||
      (this.formFeedback.value.comment == "" && this.role == "USER")
    ) {
      this.dialog.open(RemindFormReviewComponent);
    }
  }

  onClick() {
    this.dialog.open(BookingModalComponent);
  }
}
