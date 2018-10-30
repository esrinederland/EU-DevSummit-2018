// Learn more about F# at http://fsharp.org

open System
open FSharp.Data
open FSharp.Data.HttpRequestHeaders

[<EntryPoint>]
let main argv =

    let url = "http://edemo6.esri.nl/server/rest/services/TheAnswer/GPServer/TheAnswer/execute"
    let response = Http.RequestString(url,query=["f","json"], headers = [ Accept HttpContentTypes.Json ], silentHttpErrors = true)
    printfn  "%s" response


    
    let consoleInput = Console.ReadLine()

    0 // return an integer exit code
