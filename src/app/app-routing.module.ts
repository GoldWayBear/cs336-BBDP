import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { WelcomeComponent } from './welcome/welcome.component';
import { BarDetailsComponent } from './bar-details/bar-details.component';
import { DrinkerComponent } from './drinker/drinker.component';
import { BarComponent } from './bar/bar.component';
import { BeerComponent } from './beer/beer.component';
import { QueryComponent } from './query/query.component';
import { ModificationComponent } from './modification/modification.component';

const routes: Routes = [
    {
    path: '',
    pathMatch: 'full',
    redirectTo:'drinker'
  },
  {
    path: 'static',
    pathMatch: 'full',
    redirectTo: 'drinker'
  },

  {
    path:'welcome',
    pathMatch:'full',
    component:WelcomeComponent
  },


  {
    path: 'drinker',
    pathMatch: 'full',
    component: DrinkerComponent
  },
  {
    path: 'bar',
    pathMatch: 'full',
    component: BarComponent
  },
  {
      path: 'beer',
      pathMatch: 'full',
      component: BeerComponent
  },
/*  {
      path: 'query',
      pathMatch: 'full',
      component: QueryComponent
  },*/
  {
      path: 'modification',
      pathMatch: 'full',
      component: ModificationComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
