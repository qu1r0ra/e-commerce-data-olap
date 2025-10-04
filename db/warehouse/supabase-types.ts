export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.5"
  }
  public: {
    Tables: {
      DimDate: {
        Row: {
          day: number
          dayOfTheWeek: string
          fullDate: string
          id: number
          month: number
          monthName: string
          quarter: string
          year: number
        }
        Insert: {
          day: number
          dayOfTheWeek?: string
          fullDate: string
          id?: number
          month: number
          monthName?: string
          quarter?: string
          year: number
        }
        Update: {
          day?: number
          dayOfTheWeek?: string
          fullDate?: string
          id?: number
          month?: number
          monthName?: string
          quarter?: string
          year?: number
        }
        Relationships: []
      }
      DimProducts: {
        Row: {
          category: string
          createdAt: string
          description: string | null
          id: number
          name: string
          price: number
          productCode: string
          sourceId: number
          sourceSystem: Database["public"]["Enums"]["source_system"]
          updatedAt: string
        }
        Insert: {
          category?: string
          createdAt: string
          description?: string | null
          id?: number
          name: string
          price: number
          productCode?: string
          sourceId: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          updatedAt?: string
        }
        Update: {
          category?: string
          createdAt?: string
          description?: string | null
          id?: number
          name?: string
          price?: number
          productCode?: string
          sourceId?: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          updatedAt?: string
        }
        Relationships: []
      }
      DimRiders: {
        Row: {
          age: number
          courierName: string
          createdAt: string
          firstName: string
          gender: string
          id: number
          lastName: string
          sourceId: number
          sourceSystem: Database["public"]["Enums"]["source_system"]
          updatedAt: string
          vehicleType: Database["public"]["Enums"]["rider_vehicle_type"]
        }
        Insert: {
          age: number
          courierName?: string
          createdAt: string
          firstName?: string
          gender?: string
          id?: number
          lastName?: string
          sourceId: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          updatedAt?: string
          vehicleType: Database["public"]["Enums"]["rider_vehicle_type"]
        }
        Update: {
          age?: number
          courierName?: string
          createdAt?: string
          firstName?: string
          gender?: string
          id?: number
          lastName?: string
          sourceId?: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          updatedAt?: string
          vehicleType?: Database["public"]["Enums"]["rider_vehicle_type"]
        }
        Relationships: []
      }
      DimUsers: {
        Row: {
          city: string
          country: string
          createdAt: string
          dateOfBirth: string
          firstName: string
          gender: string
          id: number
          lastName: string
          sourceId: number
          sourceSystem: Database["public"]["Enums"]["source_system"]
          updatedAt: string
        }
        Insert: {
          city: string
          country: string
          createdAt: string
          dateOfBirth: string
          firstName: string
          gender: string
          id?: number
          lastName: string
          sourceId: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          updatedAt: string
        }
        Update: {
          city?: string
          country?: string
          createdAt?: string
          dateOfBirth?: string
          firstName?: string
          gender?: string
          id?: number
          lastName?: string
          sourceId?: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          updatedAt?: string
        }
        Relationships: []
      }
      ETLControl: {
        Row: {
          lastLoadTime: string
          tableName: string
        }
        Insert: {
          lastLoadTime: string
          tableName: string
        }
        Update: {
          lastLoadTime?: string
          tableName?: string
        }
        Relationships: []
      }
      FactSales: {
        Row: {
          createdAt: string
          deliveryDateId: number
          deliveryRiderId: number
          id: number
          productId: number
          quantitySold: number
          sourceId: number
          sourceSystem: Database["public"]["Enums"]["source_system"]
          userId: number
        }
        Insert: {
          createdAt: string
          deliveryDateId: number
          deliveryRiderId: number
          id?: number
          productId: number
          quantitySold: number
          sourceId: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          userId: number
        }
        Update: {
          createdAt?: string
          deliveryDateId?: number
          deliveryRiderId?: number
          id?: number
          productId?: number
          quantitySold?: number
          sourceId?: number
          sourceSystem?: Database["public"]["Enums"]["source_system"]
          userId?: number
        }
        Relationships: [
          {
            foreignKeyName: "FactSales_deliveryRiderId_fkey"
            columns: ["deliveryRiderId"]
            isOneToOne: false
            referencedRelation: "DimRiders"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "FactSales_productId_fkey"
            columns: ["productId"]
            isOneToOne: false
            referencedRelation: "DimProducts"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "FactSales_userId_fkey"
            columns: ["userId"]
            isOneToOne: false
            referencedRelation: "DimUsers"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      rider_vehicle_type: "Motorcycle" | "Bicycle" | "Tricycle" | "Car"
      source_system: "MySQL"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      rider_vehicle_type: ["Motorcycle", "Bicycle", "Tricycle", "Car"],
      source_system: ["MySQL"],
    },
  },
} as const
