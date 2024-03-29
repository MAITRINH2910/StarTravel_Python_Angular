import { Component, OnInit } from "@angular/core";
import { HttpHeaders } from "@angular/common/http";
import { AuthAccountService } from "src/app/service/auth-account.service";

@Component({
  selector: "app-view-profile-admin",
  templateUrl: "./view-profile-admin.component.html",
  styleUrls: ["./view-profile-admin.component.css"]
})
export class ViewProfileAdminComponent implements OnInit {
  private infoAdmin: any;
  public username;
  public role;

  headerConfig = {
    headers: new HttpHeaders({
      "user-access-token": window.localStorage.getItem("AuthToken")
    })
  };

  constructor(private authService: AuthAccountService) {}

  ngOnInit() {
    this.infoAdmin = this.authService
      .getInfoUser(this.headerConfig)
      .subscribe(data => {
        this.infoAdmin = data;
        this.infoAdmin = this.infoAdmin.response;
        this.role = this.infoAdmin.role;
        this.username = this.infoAdmin.username;
      });
  }
}
