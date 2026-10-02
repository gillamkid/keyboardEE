#include <XCAFApp_Application.hxx>
#include <XCAFDoc_DocumentTool.hxx>
#include <XCAFDoc_ShapeTool.hxx>
#include <XCAFDoc_ColorTool.hxx>
#include <TDocStd_Document.hxx>
#include <TDataStd_Name.hxx>
#include <BRepPrimAPI_MakeBox.hxx>
#include <STEPCAFControl_Writer.hxx>
#include <Quantity_Color.hxx>
#include <gp_Pnt.hxx>
#include <IFSelect_ReturnStatus.hxx>
int main(int argc,char**argv){
 Handle(TDocStd_Document) doc;XCAFApp_Application::GetApplication()->NewDocument("MDTV-XCAF",doc);
 auto shapes=XCAFDoc_DocumentTool::ShapeTool(doc->Main());auto colors=XCAFDoc_DocumentTool::ColorTool(doc->Main());
 auto box=[&](const char*n,double x,double y,double z,double a,double b,double c,double r,double g,double bl){
  auto l=shapes->AddShape(BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),a,b,c).Shape(),false);TDataStd_Name::Set(l,n);colors->SetColor(l,Quantity_Color(r,g,bl,Quantity_TOC_RGB),XCAFDoc_ColorGen);
 };
 // Worldsemi datasheet V1.3: 2.20 x 2.00 mm overall, central optical region 1.45 mm,
 // substrate 0.28 mm and total height 0.84 mm. Internal die depiction is illustrative.
 box("substrate",-1.1,-1,0,2.2,2,.28,.12,.12,.12);
 box("optical encapsulation",-.725,-1,.28,1.45,2,.56,.85,.85,.78);
 for(int i=0;i<4;i++){
  double x=i<2?-1.1:.725;double y=(i%2==0)?-.90:.20;
  box("solder terminal",x,y,0,.375,.7,.285,.72,.72,.70);
 }
 // Pin 1 is upper left in the KiCad footprint orientation (180 deg from datasheet top view).
 box("IC depiction",-.25,.15,.82,.5,.5,.02,.06,.06,.06);
 box("red die depiction",-.45,-.55,.82,.2,.25,.02,.72,.15,.15);
 box("green die depiction",-.10,-.55,.82,.2,.25,.02,.15,.65,.25);
 box("blue die depiction",.25,-.55,.82,.2,.25,.02,.15,.3,.75);
 shapes->UpdateAssemblies();STEPCAFControl_Writer w;w.SetColorMode(true);w.SetNameMode(true);w.Transfer(doc,STEPControl_AsIs);return w.Write(argv[1])==IFSelect_RetDone?0:1;
}
