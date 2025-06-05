from pylsl import resolve_stream, StreamInlet

def list_all_streams():
    print("🔍 Resolving all available LSL streams...")
    streams = resolve_stream()  # No filter — lists ALL types
    if not streams:
        print("❌ No LSL streams found.")
        return

    print(f"✅ Found {len(streams)} stream(s):")
    for i, stream in enumerate(streams):
        info = stream
        print(f"\n🔹 Stream #{i}")
        print(f"  Name: {info.name()}")
        print(f"  Type: {info.type()}")
        print(f"  Source ID: {info.source_id()}")
        print(f"  Channel Count: {info.channel_count()}")
        print(f"  Sampling Rate: {info.nominal_srate()} Hz")
        print(f"  Manufacturer: {info.desc().child_value('manufacturer')}")
        print(f"  Stream ID: {info.uid()}")

# Call the function
if __name__ == "__main__":
    list_all_streams()
